from flask import Flask, render_template

app = Flask(__name__)
# Help determine the root path

# @signifies a decorator - way to wrap a function and modifying its behavior
@app.route('/')
@app.route('/<user>')
def index(user=None):
    return render_template("user.html",user=user)

@app.route('/shopping')
def shopping():
    food = ["cheese", "Tuna", "Beef","toothpaste"]
    return render_template("shopping.html", food=food)


@app.route('/bacon', methods=['GET', 'POST'])
def bacon():
    if request.method == 'POST':
        return 'YOU ARE USING POST'
    else:
        return "You are probably using GET"

@app.route('/profile/<username>')
def profile(username):
    return render_template("profile.html", name=username)

@app.route('/post/<int:post_id>')
def post(post_id):
    return 'Post Id is %s' % post_id

# if __name__ == "__main__":
#     app.debug = True
#     app.run(host = '0.0.0.0', port = 8000)
