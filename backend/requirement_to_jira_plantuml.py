from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/api/convertReqToJira', methods=['POST'])
def convert_requirements_to_jiras_and_plantuml():
    """
    Please input you requirement
    ---
    parameters:
      - name: requirements
        in: body
        name: body
        required: true
        schema:
          id: requirement
          required:
            - requirement
          properties:
            requirement:
              type: string
              description: The requirement to be converted
              default: ""
    responses:
      200:
        description: input your requirement and return a jira list and plantuml
        schema:
          id:  jiraListAndPlantumlResponse
          properties:
            jiras:
              type: array
              items:
                type: string
              description: The jira list
            plantuml:
              type: string
              description: The PlantUml diagram
    """
    data = request.get_json()

    # 检查是否存在 'requirement' 参数
    if 'requirement' in data:
        requirement = data['requirement']
        # 在这里处理 requirement 参数
        return jsonify({"message": f"处理成功，requirement 参数为：{requirement}"})
    else:
        return jsonify({"error": "缺少 'requirement' 参数"}), 400


if __name__ == '__main__':
    app.run(debug=True)
