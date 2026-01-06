from fastapi import HTTPException, status


def require_role(required_role: str):
    def checker(context):
        role = context["role"]

        if role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_role} role",
            )

        return context

    return checker
