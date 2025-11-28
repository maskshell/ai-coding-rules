# Shell 脚本开发规范

## 技术栈

### 核心工具

- **Bash 4.0+**：主要使用的 Shell 解释器
- **shellcheck**：Shell 脚本静态分析工具
- **shfmt**：Shell 脚本格式化工具

### 代码质量工具

- **shellcheck**：检测常见错误和最佳实践违规
- **shfmt**：统一代码格式
- **bashate**：Bash 脚本风格检查（可选）

### 平台支持

- **Linux**：主要开发平台，使用 GNU 工具
- **macOS**：支持，但需要注意 BSD 工具差异
- **其他 Unix 系统**：尽可能保持兼容

## 项目结构

### 脚本组织方式

```text
scripts/
├── bin/                    # 可执行脚本
│   ├── deploy-app.sh
│   ├── backup-db.sh
│   └── setup-env.sh
├── lib/                    # 库函数
│   ├── logging.sh
│   ├── utils.sh
│   └── compatibility.sh
├── config/                 # 配置文件
│   └── app.conf
├── logs/                   # 日志文件
│   └── app.log
└── tests/                  # 测试脚本
    └── test_utils.sh
```

### 配置文件管理

- 配置文件使用 `.conf` 或 `.env` 扩展名
- 敏感配置使用环境变量
- 提供配置模板文件（`.conf.example`）

### 日志文件位置

- 日志文件放在 `logs/` 目录
- 使用日期命名日志文件（如 `app-2024-01-15.log`）
- 实现日志轮转机制

## 详细规范

### Shebang 和基础设置

#### 为什么使用 `#!/usr/bin/env bash`

`/usr/bin/env` 会在 PATH 中查找 bash，而不是硬编码路径。这提高了脚本的可移植性，特别是在不同系统上 bash 可能安装在不同位置。

```bash
#!/usr/bin/env bash
```

#### set -euo pipefail 的作用

- `set -e`：任何命令返回非零退出码时，脚本立即退出
- `set -u`：使用未定义的变量时报错
- `set -o pipefail`：管道中任何命令失败都返回失败状态

这三个选项组合使用，可以及早发现错误，避免脚本在错误状态下继续执行。

```bash
#!/usr/bin/env bash
set -euo pipefail
```

### 命名规范

#### 文件名规范

使用 kebab-case（短横线分隔）的原因：

- 在命令行中更易读
- 避免空格和特殊字符问题
- 符合 Unix 传统

```bash
# Good
deploy-app.sh
backup-database.sh
setup-environment.sh

# Bad
deployApp.sh          # camelCase 不符合 Unix 习惯
deploy_app.sh        # 下划线在命令行中不如短横线清晰
```

#### 函数命名规范

使用 snake_case（下划线分隔）的原因：

- Bash 函数名不支持短横线
- 下划线是 Bash 函数命名的标准做法
- 与变量命名保持一致

```bash
# Good
deploy_application() {
  # ...
}

# Bad
deployApplication() {  # 不符合 Bash 习惯
  # ...
}
```

#### 变量命名规范

- **常量**：UPPER_SNAKE_CASE，使用 `readonly` 声明
- **普通变量**：snake_case，使用 `local` 声明（函数内）

```bash
# 常量
readonly MAX_RETRIES=3
readonly CONFIG_FILE="/etc/app.conf"

# 函数内变量
my_function() {
  local user_name="admin"
  local retry_count=0
}
```

### 代码组织

#### 脚本结构模板

标准的脚本结构有助于提高可读性和可维护性：

```bash
#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# 脚本信息
# ============================================================================
# 脚本名称: deploy-app.sh
# 用途: 部署应用到生产环境
# 作者: Your Name
# 版本: 1.0.0
# 用法: ./deploy-app.sh [environment]

# ============================================================================
# 常量定义
# ============================================================================
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="${SCRIPT_DIR}/../logs/deploy.log"
readonly MAX_RETRIES=3

# ============================================================================
# 函数定义
# ============================================================================
log_info() {
  echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "${LOG_FILE}"
}

deploy_application() {
  log_info "开始部署应用"
  # 部署逻辑
}

# ============================================================================
# 主逻辑
# ============================================================================
main() {
  local environment="${1:-production}"
  deploy_application "${environment}"
}

main "$@"
```

### 错误处理

#### trap 的使用场景

`trap` 用于注册清理函数，在脚本退出时自动执行：

```bash
cleanup() {
  local exit_code=$?
  
  # 清理临时文件
  if [[ -f "${TEMP_FILE:-}" ]]; then
    rm -f "${TEMP_FILE}"
  fi
  
  # 记录错误
  if [[ ${exit_code} -ne 0 ]]; then
    log_error "脚本执行失败，退出码: ${exit_code}"
  fi
  
  exit ${exit_code}
}

trap cleanup EXIT ERR
```

#### 错误退出码规范

使用有意义的退出码有助于调用者判断错误类型：

- `0`：成功
- `1`：一般错误
- `2`：用法错误（参数错误）
- `3-125`：特定错误类型
- `126`：命令不可执行
- `127`：命令未找到
- `128+`：信号退出

### 调试和日志

#### 日志级别实现

实现统一的日志级别系统：

```bash
readonly LOG_LEVEL="${LOG_LEVEL:-INFO}"

log_debug() {
  if [[ "${LOG_LEVEL}" == "DEBUG" ]]; then
    echo "[DEBUG] $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
  fi
}

log_info() {
  if [[ "${LOG_LEVEL}" == "DEBUG" ]] || [[ "${LOG_LEVEL}" == "INFO" ]]; then
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
  fi
}

log_warn() {
  if [[ "${LOG_LEVEL}" != "ERROR" ]]; then
    echo "[WARN] $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
  fi
}

log_error() {
  echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
}
```

### 性能优化

#### 减少子进程调用

每次调用外部命令都会创建子进程，开销较大。优先使用 Bash 内置功能：

```bash
# Bad: 使用外部命令
local count=$(echo "${array[@]}" | wc -w)

# Good: 使用内置功能
local count=${#array[@]}
```

#### 批量操作优化

使用数组批量处理，减少循环中的外部命令调用：

```bash
# Good: 批量处理
readarray -t files < <(find . -name "*.txt")
for file in "${files[@]}"; do
  process_file "${file}"
done

# Bad: 在循环中调用 find
for file in $(find . -name "*.txt"); do
  process_file "${file}"
done
```

### 安全规范

#### 输入验证

所有外部输入都必须验证：

```bash
# 验证参数
if [[ $# -lt 1 ]]; then
  echo "错误: 缺少参数" >&2
  exit 1
fi

readonly input_file="$1"

# 验证文件存在
if [[ ! -f "${input_file}" ]]; then
  echo "错误: 文件不存在: ${input_file}" >&2
  exit 1
fi

# 验证文件权限
if [[ ! -r "${input_file}" ]]; then
  echo "错误: 文件不可读: ${input_file}" >&2
  exit 1
fi
```

#### 路径处理安全

防止路径注入攻击：

```bash
# 规范化路径
readonly user_path="$1"
readonly base_dir="/opt/app"

# 验证路径在允许范围内
if [[ "${user_path}" != "${base_dir}"/* ]]; then
  echo "错误: 路径不在允许范围内" >&2
  exit 1
fi

# 使用 realpath 规范化（如果可用）
if command -v realpath >/dev/null 2>&1; then
  readonly safe_path=$(realpath "${user_path}")
else
  readonly safe_path=$(cd "${user_path}" && pwd)
fi
```

#### 命令注入防护

避免直接执行用户输入：

```bash
# Good: 使用参数数组
readonly cmd=("git" "log" "--format=%H" "${user_input}")
"${cmd[@]}"

# Bad: 直接执行用户输入
eval "git log --format=%H ${user_input}"  # 危险！
```

### 跨平台兼容性

#### 工具版本检测

检测工具版本和类型：

```bash
is_gnu_command() {
  local cmd="$1"
  if "${cmd}" --version >/dev/null 2>&1; then
    return 0  # GNU
  else
    return 1  # BSD
  fi
}

# 检测操作系统
detect_os() {
  case "$(uname -s)" in
    Linux*)     echo "linux" ;;
    Darwin*)    echo "macos" ;;
    FreeBSD*)   echo "freebsd" ;;
    *)          echo "unknown" ;;
  esac
}
```

#### sed 兼容性处理

GNU sed 和 BSD sed 在 `-i` 选项上有差异：

```bash
# 兼容性包装函数
safe_sed_replace() {
  local pattern="$1"
  local replacement="$2"
  local file="$3"

  if is_gnu_command sed; then
    sed -i "s|${pattern}|${replacement}|g" "${file}"
  else
    # BSD sed (macOS)
    sed -i '' "s|${pattern}|${replacement}|g" "${file}"
  fi
}
```

#### date 兼容性处理

GNU date 和 BSD date 在日期计算上有差异：

```bash
# 获取昨天日期
get_yesterday() {
  if is_gnu_command date; then
    date -d "1 day ago" +%Y-%m-%d
  else
    date -v-1d +%Y-%m-%d
  fi
}
```

## 开发流程

### 脚本开发步骤

1. **先实现基本功能**：让脚本能正常工作，完成核心需求
   - 实现主要逻辑
   - 确保基本功能可用

2. **添加错误处理**：使用 `set -euo pipefail`，添加输入验证和错误检查
   - 添加参数验证
   - 添加文件存在性检查
   - 添加错误退出码

3. **添加日志和调试**：实现日志函数，支持调试模式
   - 实现统一的日志函数
   - 添加调试模式支持
   - 添加日志级别控制

4. **优化性能**：减少子进程调用，使用内置命令
   - 使用 Bash 内置功能
   - 批量处理优化
   - 减少循环中的外部命令调用

5. **加强安全**：验证输入，处理路径，保护敏感信息
   - 输入验证
   - 路径处理安全
   - 敏感信息保护

6. **处理兼容性**：检测环境，提供跨平台支持
   - 检测操作系统和工具版本
   - 提供兼容性包装函数
   - 在多个平台上测试

7. **编写测试**：手动测试各种场景，验证边界情况
   - 正常场景测试
   - 边界情况测试
   - 错误场景测试

8. **代码审查和重构**：改善代码结构和可读性
   - 提取重复代码为函数
   - 改善变量命名
   - 添加注释说明

### 功能开发原则

- **优先实现 MVP**：先让脚本能工作，再逐步完善
- **快速验证**：每个功能完成后立即测试
- **小步提交**：保持小的提交粒度，便于回滚
- **持续重构**：通过重构改善代码质量，不是一次完美
- **关注安全**：从一开始就考虑安全性，而不是事后补救

### 测试方法

#### 手动测试

- 在目标平台上直接运行脚本
- 测试正常场景、边界情况和错误场景
- 验证日志输出和错误处理

#### 使用 shellcheck

```bash
# 安装 shellcheck
# macOS: brew install shellcheck
# Linux: apt-get install shellcheck 或 yum install shellcheck

# 检查脚本
shellcheck script.sh

# 检查所有脚本
find . -name "*.sh" -exec shellcheck {} \;
```

#### 使用 shfmt

```bash
# 安装 shfmt
# macOS: brew install shfmt
# Linux: 从 https://github.com/mvdan/sh/releases 下载

# 格式化脚本
shfmt -w script.sh

# 检查格式
shfmt -d script.sh
```

## 工具配置

### shellcheck 配置

创建 `.shellcheckrc` 配置文件：

```bash
# .shellcheckrc
# 忽略特定警告
disable=SC2034,SC2086

# 指定 Shell 版本
shell=bash
```

### shfmt 配置

创建 `.editorconfig` 或使用命令行选项：

```bash
# 格式化选项
shfmt -i 2 -bn -ci -sr script.sh

# -i 2: 缩进 2 个空格
# -bn: 二进制操作符前不换行
# -ci: case 语句缩进
# -sr: 重定向操作符后不空格
```

### Git hooks 设置

创建 `.git/hooks/pre-commit`：

```bash
#!/bin/bash
set -e

# 运行 shellcheck
find . -name "*.sh" -exec shellcheck {} \;

# 检查格式
find . -name "*.sh" -exec shfmt -d {} \;
```

## 示例脚本

### 完整的部署脚本示例

```bash
#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# 脚本信息
# ============================================================================
# 脚本名称: deploy-app.sh
# 用途: 部署应用到指定环境
# 作者: Your Name
# 版本: 1.0.0
# 用法: ./deploy-app.sh [environment]

# ============================================================================
# 常量定义
# ============================================================================
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="${SCRIPT_DIR}/../logs/deploy.log"
readonly MAX_RETRIES=3
readonly DEFAULT_ENV="production"

# ============================================================================
# 函数定义
# ============================================================================

# 日志函数
log_info() {
  echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "${LOG_FILE}"
}

log_error() {
  echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "${LOG_FILE}" >&2
}

# 清理函数
cleanup() {
  local exit_code=$?
  if [[ ${exit_code} -ne 0 ]]; then
    log_error "部署失败，退出码: ${exit_code}"
  fi
  exit ${exit_code}
}

trap cleanup EXIT ERR

# 部署函数
deploy_application() {
  local environment="$1"
  log_info "开始部署应用到环境: ${environment}"
  
  # 部署逻辑
  # ...
  
  log_info "部署完成"
}

# 参数验证
validate_arguments() {
  if [[ $# -gt 1 ]]; then
    log_error "用法: $0 [environment]"
    exit 2
  fi
}

# ============================================================================
# 主逻辑
# ============================================================================
main() {
  validate_arguments "$@"
  
  local environment="${1:-${DEFAULT_ENV}}"
  deploy_application "${environment}"
}

main "$@"
```

### 常见场景模板

#### 配置文件处理

```bash
read_config() {
  local config_file="$1"
  local key="$2"
  
  if [[ ! -f "${config_file}" ]]; then
    log_error "配置文件不存在: ${config_file}"
    return 1
  fi
  
  grep "^${key}=" "${config_file}" | cut -d'=' -f2-
}
```

#### 文件备份

```bash
backup_file() {
  local file="$1"
  local backup_dir="${2:-./backups}"
  
  if [[ ! -f "${file}" ]]; then
    log_error "文件不存在: ${file}"
    return 1
  fi
  
  mkdir -p "${backup_dir}"
  local backup_file="${backup_dir}/$(basename "${file}").$(date +%Y%m%d_%H%M%S)"
  cp "${file}" "${backup_file}"
  log_info "文件已备份: ${backup_file}"
}
```

#### 重试机制

```bash
retry_command() {
  local max_retries="${1:-3}"
  local delay="${2:-1}"
  shift 2
  local cmd=("$@")
  
  local attempt=1
  while [[ ${attempt} -le ${max_retries} ]]; do
    if "${cmd[@]}"; then
      return 0
    fi
    
    log_warn "命令失败，重试 ${attempt}/${max_retries}: ${cmd[*]}"
    sleep "${delay}"
    ((attempt++))
  done
  
  log_error "命令失败，已达到最大重试次数: ${cmd[*]}"
  return 1
}
```

## 参考资料

- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [Bash Guide for Beginners](https://tldp.org/LDP/Bash-Beginners-Guide/html/)
- [ShellCheck Documentation](https://github.com/koalaman/shellcheck)
- [shfmt Documentation](https://github.com/mvdan/sh)
- [Bash Pitfalls](https://mywiki.wooledge.org/BashPitfalls)
