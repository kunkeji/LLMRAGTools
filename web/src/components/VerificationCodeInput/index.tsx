import React, { useState, useRef, useEffect } from 'react';
import { Input } from 'antd';
import type { InputRef } from 'antd/lib/input';
import styles from './index.less';

interface VerificationCodeInputProps {
  length?: number;
  onChange?: (code: string) => void;
}

const VerificationCodeInput: React.FC<VerificationCodeInputProps> = ({
  length = 6,
  onChange,
}) => {
  const [code, setCode] = useState<string[]>(Array(length).fill(''));
  const inputRefs = useRef<(InputRef | null)[]>([]);

  useEffect(() => {
    inputRefs.current = inputRefs.current.slice(0, length);
  }, [length]);

  const handleChange = (index: number, value: string) => {
    const newCode = [...code];
    newCode[index] = value.slice(-1);
    setCode(newCode);

    // 自动跳转到下一个输入框
    if (value && index < length - 1) {
      inputRefs.current[index + 1]?.focus();
    }

    // 触发onChange事件
    onChange?.(newCode.join(''));
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !code[index] && index > 0) {
      // 当前输入框为空且按下删除键时，跳转到上一个输入框
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault();
    const pastedData = e.clipboardData.getData('text').slice(0, length);
    const newCode = [...code];
    
    for (let i = 0; i < pastedData.length; i++) {
      newCode[i] = pastedData[i];
    }
    
    setCode(newCode);
    onChange?.(newCode.join(''));
    
    // 聚焦到最后一个有值的输入框
    const lastIndex = Math.min(pastedData.length, length) - 1;
    if (lastIndex >= 0) {
      inputRefs.current[lastIndex]?.focus();
    }
  };

  return (
    <div className={styles.container}>
      {Array(length)
        .fill(0)
        .map((_, index) => (
          <Input
            key={index}
            ref={(el) => (inputRefs.current[index] = el)}
            className={styles.input}
            value={code[index]}
            onChange={(e) => handleChange(index, e.target.value)}
            onKeyDown={(e) => handleKeyDown(index, e)}
            onPaste={handlePaste}
            maxLength={1}
          />
        ))}
    </div>
  );
};

export default VerificationCodeInput;
