from fastapi import FastAPI
from middleware.timing import TimingMiddleware
from routers import auth, users, posts, comments, tags

app = FastAPI(title="Challenge CRUD FastAPI")

app.add_middleware(TimingMiddleware)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(tags.router, prefix="/tags", tags=["Tags"])
