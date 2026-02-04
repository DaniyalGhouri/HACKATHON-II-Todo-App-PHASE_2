# Data Model: User

## Entity: User

Represents a registered user of the system. Managed primarily by Better Auth.

### Attributes

| Field | Type | Required | Description | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String | Yes | Unique Identifier | Primary Key |
| `email` | String | Yes | User Email | Unique, Valid Email |
| `emailVerified` | Boolean | Yes | Email Verification Status | Default `False` |
| `name` | String | Yes | Display Name | Max length 255 |
| `image` | String | No | Avatar URL | Nullable |
| `createdAt` | DateTime | Yes | Creation timestamp | Default `Now()` |
| `updatedAt` | DateTime | Yes | Last update | Default `Now()` |

### Notes
- This table is created/managed by Better Auth's adapter (SQLAlchemy/SQLModel compatible schema).
- Password hash is stored in a separate `account` or internal field managed by Better Auth, not directly exposed in the minimal User model used for business logic.

### Backend Representation (Pydantic/SQLModel)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    image: Optional[str] = None
    emailVerified: bool = False
    createdAt: datetime
    updatedAt: datetime
```
