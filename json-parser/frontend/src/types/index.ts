// 基础 JSON 类型
export type JsonValue = string | number | boolean | null | JsonObject | JsonArray;

export interface JsonObject {
  [key: string]: JsonValue;
}

export type JsonArray = JsonValue[];

// 应用状态
export interface AppState {
  input: string;
  output: string;
  isValid: boolean;
  errorMessage: string;
}

// 输入数据
export interface InputData {
  json: string;
  size: number;
  lineCount: number;
}

// 输出数据
export interface OutputData {
  json: string;
  formatted: boolean;
  compressed: boolean;
  indent: number;
}

// 通知消息
export interface Notification {
  type: 'success' | 'error' | 'info';
  message: string;
  duration?: number;
}

// 结果类型
export type Result<T> = { success: true; data: T } | { success: false; error: string };

// 字段校验相关类型
export interface ColumnMismatch {
  position: number;
  reader_field: string | null;
  writer_field: string | null;
}

export interface ContentValidateResult {
  index: number;
  valid: boolean;
  reader_count: number;
  writer_count: number;
  mismatches: ColumnMismatch[];
}

export interface ColumnValidateResponse {
  valid: boolean;
  results: ContentValidateResult[];
}
