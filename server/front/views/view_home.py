from flask import render_template


def create(view_app):
    @view_app.route('/')
    @view_app.route('/home')
    def view_home():
        """Renders the home page."""
        return render_template(
            'index.html',
            title='Home Page',
            author='Sohn, Joon Sung',
            year='2018-09-18'
        )