from flask_admin.contrib.sqla import ModelView
from flask_security import current_user


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


class UserView(ModelView):
    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('admin') or current_user.has_role('end-user')
