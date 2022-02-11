class NhlAppRouter:
    route_app_labels = {'nhl_app'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'nhl_app'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'nhl_app'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        label_1 = obj1._meta.app_label
        label_2 = obj2._meta.app_label
        labels = self.route_app_labels
        if (label_1 in labels or label_2 in labels):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'nhl_app'
        return None


class AuthRouter:
    route_app_labels = {'auth', 'contenttypes'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'django_nhl_app'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'django_nhl_app'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        label_1 = obj1._meta.app_label
        label_2 = obj2._meta.app_label
        labels = self.route_app_labels
        if (label_1 in labels or label_2 in labels):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'django_nhl_app'
        return None
