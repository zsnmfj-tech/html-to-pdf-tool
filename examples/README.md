# 使用示例

本目录包含HTML转PDF工具的使用示例。

## 示例文件

- `index.html` - 一个真实的HTML文件示例(包含中文内容和样式)
- `index.pdf` - 转换后的PDF文件

## 如何运行示例

### 方法一:使用命令行工具

```bash
# 基本转换
html2pdf examples/index.html

# 指定输出文件
html2pdf examples/index.html -o examples/output.pdf

# 启用详细输出
html2pdf examples/index.html -v
```

### 方法二:直接运行Python脚本

```bash
python src/html_to_pdf.py examples/index.html -o examples/output.pdf -v
```

### 方法三:在Python代码中使用

```python
from html_to_pdf import convert_html_to_pdf

# 转换示例文件
convert_html_to_pdf('examples/index.html', 'examples/output.pdf')
```

## 注意事项

1. **相对路径资源**:如果HTML文件引用了相对路径的CSS、图片等资源,工具会自动使用HTML文件所在目录作为基础路径。

2. **中文支持**:工具完全支持中文内容,确保HTML文件使用UTF-8编码。

3. **样式保留**:内联样式和外部CSS文件都会被正确转换到PDF中。

4. **文件大小**:生成的PDF文件大小取决于HTML内容的复杂度和嵌入的资源。
