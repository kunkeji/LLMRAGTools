import { IDomEditor } from '@wangeditor/editor';
import { message } from 'antd';
import { Boot } from '@wangeditor/editor';

// 自定义菜单类
class CustomButtonMenu {
  readonly title: string;
  readonly tag: string;

  constructor() {
    this.title = 'AI帮写';
    this.tag = 'button';
  }

  getValue(): string | boolean {
    return '';
  }

  isActive(): boolean {
    return false;
  }

  isDisabled(): boolean {
    return false;
  }

  exec(editor: IDomEditor) {
    message.success('你好');
  }
}

// 注册自定义菜单
Boot.registerMenu({
  key: 'customButton',
  factory() {
    return new CustomButtonMenu();
  },
});

export const CUSTOM_BUTTON_KEY = 'customButton';