import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Modal, Form, Select, Input, message, Space, Tooltip } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import { llmApi } from '@/services/api/llm';
import type { Feature, FeatureMapping } from '@/services/api/llm';
import styles from './index.less';

const { TextArea } = Input;

const MappingPage: React.FC = () => {
  const [form] = Form.useForm();
  const [features, setFeatures] = useState<Feature[]>([]);
  const [mappings, setMappings] = useState<FeatureMapping[]>([]);
  const [channels, setChannels] = useState<API.LLMChannel[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [currentFeature, setCurrentFeature] = useState<Feature>();
  const [submitting, setSubmitting] = useState(false);

  // 加载数据
  const loadData = async () => {
    try {
      setLoading(true);
      const [featuresData, mappingsData, channelsData] = await Promise.all([
        llmApi.getFeatures(),
        llmApi.getFeatureMappings(),
        llmApi.getChannels(),
      ]);
      setFeatures(featuresData);
      setMappings(mappingsData);
      setChannels(channelsData);
    } catch (error: any) {
      message.error(error.message || '加载数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // 处理编辑功能映射
  const handleEdit = (feature: Feature) => {
    setCurrentFeature(feature);
    const mapping = mappings.find(m => m.feature_type === feature.feature_type);
    form.setFieldsValue({
      llm_model_id: mapping?.llm_model_id,
      prompt_template: mapping?.prompt_template || feature.default_prompt,
    });
    setModalVisible(true);
  };

  // 处理保存功能映射
  const handleSave = async (values: any) => {
    if (!currentFeature) return;
    try {
      setSubmitting(true);
      await llmApi.saveFeatureMapping({
        feature_type: currentFeature.feature_type,
        llm_model_id: values.llm_model_id,
        prompt_template: values.prompt_template,
      });
      message.success('保存成功');
      setModalVisible(false);
      loadData();
    } catch (error: any) {
      message.error(error.message || '保存失败');
    } finally {
      setSubmitting(false);
    }
  };

  const columns = [
    {
      title: '功能名称',
      dataIndex: 'name',
      key: 'name',
      width: 150,
    },
    {
      title: '功能说明',
      dataIndex: 'description',
      key: 'description',
      width: 200,
    },
    {
      title: '当前渠道',
      key: 'model',
      width: 150,
      render: (_: any, record: Feature) => {
        const mapping = mappings.find(m => m.feature_type === record.feature_type);
        const channel = channels.find(c => c.id === mapping?.llm_model_id);
        return channel ? `${channel.channel_name} (${channel.model})` : '-';
      },
    },
    {
      title: '使用次数',
      key: 'use_count',
      width: 100,
      render: (_: any, record: Feature) => {
        const mapping = mappings.find(m => m.feature_type === record.feature_type);
        return mapping?.use_count || 0;
      },
    },
    {
      title: '最后使用时间',
      key: 'last_used_at',
      width: 180,
      render: (_: any, record: Feature) => {
        const mapping = mappings.find(m => m.feature_type === record.feature_type);
        return mapping?.last_used_at ? new Date(mapping.last_used_at).toLocaleString() : '-';
      },
    },
    {
      title: '操作',
      key: 'action',
      width: 100,
      render: (_: any, record: Feature) => (
        <Button type="link" onClick={() => handleEdit(record)}>
          配置
        </Button>
      ),
    },
  ];

  return (
    <div className={styles.container}>
      <Card title="功能映射">
        <Table
          columns={columns}
          dataSource={features}
          rowKey="feature_type"
          loading={loading}
          pagination={false}
        />
      </Card>

      <Modal
        title="配置功能映射"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
        >
          <Form.Item
            name="llm_model_id"
            label="选择渠道"
            rules={[{ required: true, message: '请选择渠道' }]}
          >
            <Select
              placeholder="请选择渠道"
              options={channels.map(channel => ({
                label: `${channel.channel_name} (${channel.model})`,
                value: channel.id,
              }))}
            />
          </Form.Item>

          <Form.Item
            label={
              <Space>
                提示词模板
                <Tooltip title="不填则使用默认模板">
                  <QuestionCircleOutlined />
                </Tooltip>
              </Space>
            }
            name="prompt_template"
          >
            <TextArea
              placeholder="请输入提示词模板"
              autoSize={{ minRows: 4, maxRows: 8 }}
            />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={submitting}>
                保存
              </Button>
              <Button onClick={() => setModalVisible(false)}>取消</Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default MappingPage; 