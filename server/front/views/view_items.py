from flask import render_template



def create(view_app):
    @view_app.route('/dev/itemlist')
    def view_itemlist():
        """Renders the home page."""

        return render_template(
            'itemlist.html'
        )
