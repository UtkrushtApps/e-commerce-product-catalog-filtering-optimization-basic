# Task Overview

The e-commerce product catalog FastAPI application manages products, categories, and brands. As customers shop, filtering products by both category and brand is a critical feature, but currently, the response times are extremely slow (~3-4 seconds) when these filters are applied together. This severely affects user experience and business outcomes.

## Guidance

- You are provided a fully functional FastAPI app, including async endpoints for listing products with optional filtering by category and brand.
- The codebase already includes basic async logic using raw SQL with psycopg2; you do NOT need to set up routes or scaffolding.
- Product-listing queries with both category and brand filters are slow due to suboptimal PostgreSQL schema and query structures.
- The likely performance issues involve full table scans caused by missing or poorly chosen indexes and inefficient SQL query structure for filtering.
- Review the schema design: check if filter columns are indexed or if a composite index is missing for the multi-column filter case.
- Use EXPLAIN or your preferred database analysis tools to validate query performance.
- Focus only on database structure and related logic—do not change the FastAPI routes or overall app structure.

## Database Access
- **Host**: <DROPLET_IP>
- **Port**: 5432
- **Database name**: ecommerce_db
- **Username**: fastapi_user
- **Password**: fastapi_pass

You can use tools like pgAdmin, DBeaver, or psql to analyze and verify query performance.

## Objectives
- Identify and fix performance bottlenecks in product filtering by category and brand.
- Ensure that queries affected by multi-column WHERE clauses use efficient execution paths (e.g., index scans, not sequential scans).
- Improve schema design with appropriate indexes and constraints to support fast filtering and maintain normalized relationships between products, categories, and brands.

## How to Verify
- Compare the response times for GET /products?category_id=...&brand_id=... before and after optimization—they should drop from 3-4 seconds to < 500ms.
- Use EXPLAIN ANALYZE against the filtering query to confirm that index scans replace sequential scans.
- Check with bulk product data: API performance should remain acceptable as the data volume increases.
- Database metrics (pg_stat_statements, query plans) should show improved execution statistics for key endpoints.