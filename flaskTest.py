from flask import Flask, render_template, request
import searchDoc

app = Flask(__name__)  # 一个Flask类的对象
app.debug = False

@app.route('/searchNov', methods=['GET', "POST"])
def index1():
    keyword = []
    temp = ""
    if request.method == 'POST':
        temp = request.form.get('Name')  # 获取POST传过来的值
        keyword.append(temp)
    if temp != "":
        result = searchDoc.search(keyword)
        print(result)
        if len(result) != 0:
            return render_template('result.html', URL=result, novelsName=temp)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
