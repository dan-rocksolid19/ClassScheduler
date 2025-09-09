current_user = None


def login(user):
    global current_user
    current_user = user
    print(f"SESSION: User logged in - {user.username} (ID: {user.id})")


def logout():
    global current_user
    if current_user:
        print(f"SESSION: User logged out - {current_user.username} (ID: {current_user.id})")
    else:
        print("SESSION: Logout called but no user was logged in")
    current_user = None


def login_required(func):
    def wrapper(*args, **kwargs):
        if current_user is None:
            print("SESSION: login_required decorator - No current user found")
            raise PermissionError("login required")
        print(f"SESSION: login_required decorator - User authenticated: {current_user.username}")
        return func(*args, **kwargs)
    return wrapper 