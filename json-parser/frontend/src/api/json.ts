/**
 * JSON API 工具
 * 通过 HTTP 调用后端 API 提供 JSON 格式化、压缩和验证功能
 */

import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/json'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const jsonApi = {
  /**
   * 格式化 JSON
   * @param json JSON 字符串
   * @param indent 缩进空格数或制表符，默认 2
   * @returns 格式化后的 JSON 字符串
   */
  format(json: string, indent: number | string = 2): Promise<string> {
    return api.post('/format', { json, indent })
      .then(res => res.data.formatted)
  },

  /**
   * 压缩 JSON
   * @param json JSON 字符串
   * @returns 压缩后的 JSON 字符串
   */
  minify(json: string): Promise<string> {
    return api.post('/minify', { json })
      .then(res => res.data.minified)
  },

  /**
   * 验证 JSON 是否有效
   * @param json JSON 字符串
   * @returns 验证结果
   */
  validate(json: string): Promise<{ valid: boolean; error?: string }> {
    return api.post('/validate', { json })
      .then(res => res.data)
  },

  /**
   * 计算 JSON 字符串大小（字节）
   * @param json JSON 字符串
   * @returns 字节大小
   */
  getSize(json: string): Promise<number> {
    return api.post('/size', { json })
      .then(res => res.data.size)
  },

  /**
   * 计算 JSON 行数
   * @param json JSON 字符串
   * @returns 行数
   */
  getLineCount(json: string): Promise<number> {
    return api.post('/lines', { json })
      .then(res => res.data.lines)
  }
}
