# accounts/middleware.py

class StoreUserInfoMiddleware:
    """
    After AuthenticationMiddleware, stash a few User fields into request.session
    so you can read them anywhere.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is logged in, store their details
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            # Overwrite (or set) these session keys on every request
            request.session["username"]    = user.username
            request.session["first_name"]  = user.first_name
            request.session["last_name"]   = user.last_name
            # Assuming your custom User model has a job_title field:
            request.session["job_title"]   = getattr(user, "job_title", "")
        response = self.get_response(request)
        return response
