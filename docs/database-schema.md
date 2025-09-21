# Database Schema

## Entity Relationship Diagram

```mermaid
erDiagram
    TRACKING_ENTRY {
        int transaction_id PK
        int category_id FK
        date date
        int unit_id FK
        int type_id FK
        int quantity
        int tag_id FK
        text comment
    }
    
    CATEGORY {
        int category_id PK
        string name
        text description
        int parent_id FK
    }
    
    UNIT {
        int unit_id PK
        string name
        string unit_type
        decimal conversion_factor
    }
    
    TYPE {
        int type_id PK
        string name
        int parent_id FK
    }
    
    TAG {
        int tag_id PK
        string name
    }
    
    TRACKING_ENTRY ||--|| CATEGORY : "belongs to"
    TRACKING_ENTRY ||--|| UNIT : "measured in"
    TRACKING_ENTRY ||--|| TYPE : "is of type"
    TRACKING_ENTRY ||--|| TAG : "tagged with"
    CATEGORY ||--o| CATEGORY : "parent/child"
    TYPE ||--o| TYPE : "parent/child"
```

## Description

- **TRACKING_ENTRIES**: Main table for all tracking entries
- **CATEGORIES**: Hierarchical categories (e.g. Sports > Running)  
- **UNITS**: Units of measurement with conversion factors
- **TYPES**: Hierarchical types (e.g. Education > Bachelor)
- **TAGS**: Flexible tags for additional categorization