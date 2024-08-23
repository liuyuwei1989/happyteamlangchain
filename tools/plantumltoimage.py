import subprocess
import os


def convert_plantuml_to_image(plantuml_text, output_file):
    # 将PlantUML文本写入临时文件
    with open('temp.puml', 'w') as f:
        f.write(plantuml_text)

    # 使用plantuml命令行工具将临时文件转换为图片
    subprocess.run(['java', '-jar', r'D:\pythonProjects\langchainjerryhelloworld\tools\plantuml-1.2024.6.jar', r'D:\pythonProjects\langchainjerryhelloworld\tools\temp.puml', '-o', output_file])

    # 删除临时文件
    os.remove('temp.puml')


# 示例PlantUML文本
plantuml_text = """
@startuml
Alice -> Bob: Hello
Bob --> Alice: Hi!
@enduml
"""

# 转换并保存为图片
convert_plantuml_to_image(plantuml_text, 'output.png')
