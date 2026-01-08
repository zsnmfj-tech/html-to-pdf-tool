# HTML to PDF Tool

一个简单易用的HTML转PDF工具,支持命令行使用和Python模块导入。

## 功能特点

- **Chromium 内核渲染**: 使用 Playwright/Chromium 引擎，确保 PDF 与浏览器看到的视觉效果 100% 一致。
- **智能预处理**: 自动处理 `data-src` 延迟加载图片，解决微信公众号等平台的图片丢失问题。
- **路径自动修复**: 自动将相对路径转换为绝对路径，确保本地图片、CSS 和字体完美加载。
- **高保真排版**: 完整保留复杂的 CSS 布局、字体样式和多媒体内容。
- **简单易用**: 命令行一键转换，支持自定义等待条件以确保动态内容加载完成。

## 安装

### 安装步骤

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Chromium 浏览器内核
playwright install chromium

# 安装工具
python setup.py install
```

## 使用方法

### 命令行使用

安装后,可以使用 `html2pdf` 命令:

```bash
# 基本用法:转换HTML文件
html2pdf input.html

# 指定输出文件名
html2pdf input.html -o output.pdf

# 指定基础 URL (用于解析相对路径)
html2pdf input.html -b http://example.com

# 指定等待条件 (默认为 networkidle，确保网络请求完成后再转换)
html2pdf input.html -w networkidle

# 指定输出路径
html2pdf input.html -o output.pdf

# 组合使用
html2pdf input.html -o output.pdf -b ./assets -v
```

### Python模块使用

```python
from html_to_pdf import convert_html_to_pdf

# 基本转换
convert_html_to_pdf('input.html')

# 指定输出路径
convert_html_to_pdf('input.html', output_path='output.pdf')

# 指定基础URL
convert_html_to_pdf('input.html', base_url='http://example.com')

# 添加额外CSS
convert_html_to_pdf('input.html', css_files=['style1.css', 'style2.css'])
```

## 技术说明

本工具基于 [WeasyPrint](https://weasyprint.org/) 库开发,WeasyPrint是一个智能的HTML/CSS转PDF渲染引擎,具有以下特点:

- 完整支持HTML5和CSS3规范
- 支持嵌入图片、字体和其他资源
- 支持分页、页眉页脚等PDF特性
- 纯Python实现,易于集成和扩展

## 常见问题

### 1. 相对路径资源无法加载

如果HTML文件中使用了相对路径引用CSS、图片等资源,需要使用 `-b` 参数指定基础URL:

```bash
html2pdf input.html -b file:///path/to/html/directory
```

或者使用相对路径:

```bash
html2pdf input.html -b ./
```

### 2. 字体显示问题

确保系统中安装了HTML中使用的字体,或者在CSS中使用 `@font-face` 引入字体文件。

### 3. 样式不正确

可以通过 `-c` 参数添加额外的CSS文件来调整样式:

```bash
html2pdf input.html -c fix-styles.css
```

## 依赖项

- Python >= 3.7
- WeasyPrint >= 60.0

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request!

## 项目地址

https://github.com/zsnmfj-tech/html-to-pdf-tool
