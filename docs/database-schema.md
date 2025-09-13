# Database Schema

## Entity Relationship Diagram

```mermaid
erDiagram
    TRACKING_ENTRIES {
        int transaction_id PK
        int category_id FK
        date date
        int unit_id FK
        int type_id FK
        int quantity
        int tag_id FK
        text comment
    }
    
    CATEGORIES {
        int category_id PK
        string name
        text description
        int parent_id FK
    }
    
    UNITS {
        int unit_id PK
        string name
        string unit_type
        decimal conversion_factor
    }
    
    TYPES {
        int type_id PK
        string name
        int parent_id FK
    }
    
    TAGS {
        int tag_id PK
        string name
    }
    
    TRACKING_ENTRIES ||--|| CATEGORIES : "belongs to"
    TRACKING_ENTRIES ||--|| UNITS : "measured in"
    TRACKING_ENTRIES ||--|| TYPES : "is of type"
    TRACKING_ENTRIES ||--|| TAGS : "tagged with"
    CATEGORIES ||--o| CATEGORIES : "parent/child"
    TYPES ||--o| TYPES : "parent/child"
```

## Beschreibung

- **TRACKING_ENTRIES**: Haupttabelle für alle Tracking-Einträge
- **CATEGORIES**: Hierarchische Kategorien (z.B. Sport > Laufen)
- **UNITS**: Maßeinheiten mit Konvertierungsfaktoren
- **TYPES**: Hierarchische Typen (z.B. Zeit-Tracking > Arbeit)
- **TAGS**: Flexible Tags für zusätzliche Kategorisierung