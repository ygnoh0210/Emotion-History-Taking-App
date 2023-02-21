import json

from flask import Flask, render_template, request, url_for, redirect, session
import logging
import healthbot.bot
import healthbot.bot as bot



app = Flask(__name__, static_url_path='/static')

logger = logging.getLogger('QApair')

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('./Logs/QApair.txt')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=['GET', 'POST'])
@app.route('/first_page.html', methods=['Get', 'POST'])
def first_page():
    return render_template('first_page.html')

@app.route('/login.html', methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        # password = request.form['password']
        try:
            if name != "":
                session["logged_in"] = True
                session["user_id"] = name
                session["final_entity"] = []
                session["final_intent"] = []
                # 3번을 해보세요!
                return render_template('index.html')
            else:
                return '모든 정보를 입력한 후 다시 시도하세요.'
        except:
            return 'Don\'t login'
    else:
        return render_template('login.html')

@app.route('/explain.html', methods=['Get', 'POST'])
def explain():
    return render_template('explain.html')

@app.route('/join.html', methods=['Get', 'POST'])
def join():
    if request.method == 'POST':
        name = request.form['username']
        # password = request.form['password']
        try:
            if name != "":
                session["logged_in"] = True
                session["user_id"] = name
                session["final_entity"] = []
                session["final_intent"] = []
                # 3번을 해보세요!
                return render_template('index.html')
            else:
                return '모든 정보를 입력한 후 다시 시도하세요.'
        except:
            return 'Don\'t join'
    else:
        return render_template('join.html')

# ## GET 방식으로 값을 전달받음.
# ## num이라는 이름을 가진 integer variable를 넘겨받는다고 생각하면 됨.
# ## 아무 값도 넘겨받지 않는 경우도 있으므로 비어 있는 url도 함께 mapping해주는 것이 필요함
# @app.route('/')
# def main_get(num=None):
#     return render_template('index.html')


@app.route('/index.html',)
def get_index(num=None):
    return render_template('index.html')


@app.route('/main.html', methods=['POST', 'GET'])
def main_function(num=None):
    return render_template('main.html')
    ## 어떤 http method를 이용해서 전달받았는지를 아는 것이 필요함
    ## 아래에서 보는 바와 같이 어떤 방식으로 넘어왔느냐에 따라서 읽어들이는 방식이 달라짐
    # if request.method == 'POST':
    #     #temp = request.form['num']
    #     pass
    # elif request.method == 'GET':
    #     ## 넘겨받은 질문 및 사용자 이름
    #     question = request.args.get('question')
    #     user_name = request.args.get('username')
    #
    #
    #     ## 챗봇 QA 처리 코드
    #     answer = bot.search_answer_from_bot(question)
    #
    #     ## QA logging
    #     # logging(question, answer)
    #
    #     logger.info(f'%s,%s,%s'%(user_name, question, answer))
    #
    #     ## 넘겨받은 값을 원래 페이지로 리다이렉트
    #     return render_template('main.html', question=question, answer=answer)
    ## else 로 하지 않은 것은 POST, GET 이외에 다른 method로 넘어왔을 때를 구분하기 위함


@app.route('/task1.html', methods=['POST', 'GET'])
def task1_function(num=None):
    # question = request.args.get('question')
    #
    # print(question)
    #
    # 챗봇 QA 처리 코드
    # answer = bot.search_answer_from_bot(question)
    answer = 'I AM HERE'
    ## QA logging
    # logging(question, answer)

    # logger.info(f'%s,%s'%(question, answer))
    return render_template('task1.html', bot_answer=answer)
    ## 어떤 http method를 이용해서 전달받았는지를 아는 것이 필요함
    ## 아래에서 보는 바와 같이 어떤 방식으로 넘어왔느냐에 따라서 읽어들이는 방식이 달라짐
    # if request.method == 'POST':
    #     #temp = request.form['num']
    #     pass
    # elif request.method == 'GET':
    #     ## 넘겨받은 질문 및 사용자 이름
    #     if request.method == 'POST':
    #         temp = request.form['question']
    #     else:
    #         temp = None
    #     return render_template('task1.html', question=temp)
    #
    #     question = request.args.get('question')

    # print(question)
    #
    # ## 챗봇 QA 처리 코드
    # answer = bot.search_answer_from_bot(question)
    #
    # ## QA logging
    # # logging(question, answer)
    #
    # logger.info(f'%s,%s'%(question, answer))
    #
    # ## 넘겨받은 값을 원래 페이지로 리다이렉트
    # return render_template('task1.html', question=question, answer=answer)
    ## else 로 하지 않은 것은 POST, GET 이외에 다른 method로 넘어왔을 때를 구분하기 위함


@app.route('/task2.html', methods=['POST', 'GET'])
def task2_function():
    answer="I AM HERE"
    # answer = "죄송해요. 제가 드릴 수 있는 답변이 없네요. T.T"  # default answer
    if request.method == 'POST':
        print("task2 wow")
        # question = request.form['question_id']
        # print(question)
        # answer = bot.search_answer_from_bot(question, session["final_entity"])
        # logger.info(f'%s,%s' % (question, answer))

    # print(answer)
    return render_template('task2.html', bot_answer=answer)

@app.route('/task3.html', methods=['POST', 'GET'])
def task3_function():
    answer = 'I AM HERE'
    if request.method == 'POST':
        print("task3 wow")
    return render_template('task3.html', bot_answer=answer)

@app.route('/task4.html', methods=['POST', 'GET'])
def task4_function():
    answer = 'I AM HERE'
    return render_template('task4.html', bot_answer=answer)

@app.route('/get_answer', methods=['POST', 'GET'])
def get_answer():
    if request.method == 'POST':
        question = request.form['question_id']
        title = request.form['title']
        title = title.rstrip('\n')
        # print(question, title)

        for alt in alt_list:
            # print(alt, question)
            if alt in question:
                question = question.replace(alt, title)

        # print(question)
        res, answer, session['final_entity'], session['final_intent'] = bot.search_answer_from_bot(question, session[
            'final_entity'], session['final_intent'])

        logger.info(f'%s,%s,%s,%s,%s' % (session["user_id"], title, question, res, answer))
        return answer


@app.route('/next_paging', methods=['POST', 'GET'])
def next_paging():
    if request.method == 'POST':
        paging = request.form['paging']
        now_page, total_page = paging.split('/')
        next_page = str(int(now_page) + 1)

        content = search_database(next_page)

        result = json.dumps({
            'title': content["title"],
            'text-area': content["description"],
            'li': content["li"],
            'img_url': "https://yeogyeong.pythonanywhere.com/static/image/%s.jpg" % next_page,
            'paging': next_page + '/' + total_page
        })
        return result


@app.route('/prev_paging', methods=['POST', 'GET'])
def prev_paging():
    if request.method == 'POST':
        paging = request.form['paging']
        now_page, total_page = paging.split('/')
        prev_page = str(int(now_page) - 1)

        content = search_database(prev_page)

        result = json.dumps({
            'title': content["title"],
            'text-area': content["description"],
            'li': content["li"],
            'img_url': "https://yeogyeong.pythonanywhere.com/static/image/%s.jpg" % prev_page,
            'paging': prev_page + '/' + total_page
        return result


def search_database(page_num):
    with open('./static/description/%s.txt' % page_num, 'r', encoding='UTF8') as f:
        content = f.readlines()
        title = content[0]

        li = []
        description = []
        for line in content[1:]:
            if "-" in line:
                line.replace("-", "")
                li.append(line)
            else:
                # otherwise, description
                description.append(line)

        description = "".join(description)

        return {"title": title, "li": li, "description": description}


@app.route('/next_paging_task2', methods=['POST', 'GET'])
def next_paging_task2():
    if request.method == 'POST':
        paging = request.form['paging']
        answer = request.form['user_answer']
        now_page, total_page = paging.split('/')

        logger.info(f'%s,[TASK2],%s,%s' % (session["user_id"], now_page, answer))

        next_page = str(int(now_page) + 1)

        problem = task_item[next_page]

        result = json.dumps({
            'problem': problem,
            'paging': next_page + '/' + total_page
        })
        return result


@app.route('/prev_paging_task2', methods=['POST', 'GET'])
def prev_paging_task2():
    if request.method == 'POST':
        paging = request.form['paging']
        now_page, total_page = paging.split('/')
        prev_page = str(int(now_page) - 1)

        problem = task_item[prev_page]

        result = json.dumps({
            'problem': problem,
            'paging': prev_page + '/' + total_page
        })
        return result


@app.route('/custom_logging', methods=['POST'])
def custom_logging():
    if request.method == 'POST':
        paging = request.form['paging']
        answer = request.form['user_answer']
        now_page, total_page = paging.split('/')

        logger.info(f'%s,[TASK2],%s,%s' % (session["user_id"], now_page, answer))
        return ''


if __name__ == '__main__':
    # threaded=True 로 넘기면 multiple plot이 가능해짐
    # app.run(host='172.27.185.233', port=8888, debug=True, threaded=True)
    app.run()
