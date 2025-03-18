import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from app.routes import auth, users


title = "Test task"
description = f"""
{title} helps you streamline the collection and processing of user feedback on internal services. 🚀

## Test task 

## Technical Requirements

### Authentication and Authorization with Redis

1. **JWT Token Management**:
   - Implement a system for managing JWT tokens using Redis.
   - Create **blacklist** and **whitelist** for tokens to control access.
   
2. **Role-Based Access Control (RBAC)**:
   - Implement a role system with at least two roles:
     - **Common Role**: Shared content accessible by all roles.
     - **Exclusive Role**: Content accessible only by users with this specific role.
"""

app = FastAPI(
    title=title,
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Kyrawamnedura",
        "email": "olyabjj@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = ["*"]

app.include_router(auth.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI User Management System!"}
