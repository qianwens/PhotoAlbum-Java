---
name: migration-oracle-to-postgresql
description: Migrate from Oracle DB to PostgreSQL
---

# oracle-to-postgresql

## Overview

Migrate from Oracle DB to PostgreSQL

## Knowledge Base Content

* KB ID: microsoft://database-tasks/oracle-to-postgresql/java.formula
* Title: Migrate Java code from Oracle to PostgreSQL
* Description: Update Java files for Oracle to PostgreSQL migration
* Content: 
### Search code
Search files from workspace using below patterns:
- Glob pattern to find files: `**/*.java`
- Regex pattern to find code lines: `/VARCHAR2|CLOB|BLOB|SYSDATE|ROWNUM|ROWID|NOCOPY|TABLE|PROCEDURE|CONNECT BY\s+|START WITH|BULK COLLECT|FORALL|PL\/SQL|NOCACHE|DUAL|PRAGMA|JOIN\s+|CREATE\s+|ALTER\s+|SELECT\s+|INSERT\s+|UPDATE\s+|java\.sql\.Array|@Table|@Column|@NamedNativeQuery|@SequenceGenerator|@GeneratedValue|Oracle/i`
> you could use tools to search code whatever if possible.
### Instruction


Your task is to migrate Java code from Oracle database usage to PostgreSQL compatibility.

Follow these steps:
1. Locate the `coding_notes.md` file:
  - If `coding_notes.md` is already provided in the prompt or context, use it and skip to step 2.
  - Otherwise, search for `coding_notes.md` in the migration project workspace using the pattern `.github/postgres-migrations/*/results/application_guidance/coding_notes.md`.
  - If multiple files are found, compare their modification timestamps and use the most recently modified file.
  - If no `coding_notes.md` file is found, proceed to step 3 using only the formula checklist.
2. If `coding_notes.md` is found, read its entire content before listing files that need to be migrated.
  - The file contains project-specific migration guidance and rules that must be read before listing files that need to be migrated.
  - The file may exceed 1,000 lines; ensure you read it completely from start to end.
3. Review the formula checklist items below. **Priority rule**: If any checklist item conflicts with guidance in `coding_notes.md`, follow the `coding_notes.md` instructions instead.
4. Apply each relevant modification to the file.
5. For each change, add a comment to the migrated code that includes the checklist item information. Example:
  ```java
  // Migrated from Oracle to PostgreSQL according to java check item 1: Convert all table and column names from uppercase to lowercase in JPA annotations.
  // Migrated from Oracle to PostgreSQL according to coding notes check item: All object names are lowercased in PostgreSQL (unless quoted explicitly).
  ```

## Formula checklist

Java check item 0: Don't modify the content if it's obviously not related to Oracle based on file names or paths. However, always review imports and annotations (e.g., @SequenceGenerator) to identify Oracle-specific code that may require migration.

Java check item 1: Convert all table and column names from uppercase to lowercase in JPA annotations.
  ```java
  // Before migration (Oracle)
  @Entity
  @Table(name = "ITEMS")
  public class Item {
      @Id
      @Column(name = "ITEM_ID")
      private Long id;
  }

  // After migration (PostgreSQL)
  @Entity
  @Table(name = "items")
  public class Item {
      @Id
      @Column(name = "item_id")
      private Long id;
  }
  ```

Java check item 2: Convert sequence generator names to lowercase in JPA annotations.
  ```java
  // Before migration (Oracle)
  @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "ITEM_SEQ")
  @SequenceGenerator(name = "ITEM_SEQ", sequenceName = "ITEMS_SEQ", allocationSize = 1)

  // After migration (PostgreSQL)
  @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "item_seq")
  @SequenceGenerator(name = "item_seq", sequenceName = "items_seq", allocationSize = 1)
  ```

Java check item 3: Replace Oracle-specific SQL functions with PostgreSQL equivalents. Like RANK() to ROW_NUMBER()
  ```java
  // Before migration (Oracle)
  @NamedNativeQuery(
      name = "Item.findTopItems",
      query = """
          SELECT i.* FROM (
              SELECT i.*,
                     RANK() OVER (PARTITION BY i.CATEGORY_ID ORDER BY i.PRICE DESC) as price_rank
              FROM ITEMS i
          ) i
          WHERE i.price_rank <= :topN
          ORDER BY i.CATEGORY_ID, i.price_rank
      """
  )

  // After migration (PostgreSQL)
  @NamedNativeQuery(
      name = "Item.findTopItems",
      query = """
          SELECT i.* FROM (
              SELECT i.*,
                     ROW_NUMBER() OVER (PARTITION BY i.category_id ORDER BY i.price DESC) as price_rank
              FROM items i
          ) i
          WHERE i.price_rank <= :topN
          ORDER BY i.category_id, i.price_rank
      """
  )
  ```

Java check item 4: Replace TO_CHAR date functions with EXTRACT in SQL statements.
  ```java
  // Before migration (Oracle)
  @NamedNativeQuery(
      name = "Item.findItemsCreatedInQuarter",
      query = """
          SELECT * FROM ITEMS
          WHERE TO_CHAR(CREATE_DATE, 'Q') = :quarter
          AND TO_CHAR(CREATE_DATE, 'YYYY') = :year
          ORDER BY CREATE_DATE
      """
  )

  // After migration (PostgreSQL)
  @NamedNativeQuery(
      name = "Item.findItemsCreatedInQuarter",
      query = """
          SELECT * FROM items
          WHERE EXTRACT(QUARTER FROM create_date) = CAST(:quarter AS INTEGER)
          AND EXTRACT(YEAR FROM create_date)::text = :year
          ORDER BY create_date
      """
  )
  ```

Java check item 5: Replace TRUNC(date) with DATE_TRUNC('day', date) in SQL.
  ```java
  // Before migration (Oracle)
  "SELECT * FROM EMPLOYEES WHERE TRUNC(HIRE_DATE) BETWEEN TO_DATE(:startDate, 'YYYY-MM-DD') AND TO_DATE(:endDate, 'YYYY-MM-DD')"

  // After migration (PostgreSQL)
  // IMPORTANT: Don't delete other methods like "TO_DATE"
   "SELECT * FROM employees WHERE DATE_TRUNC('day', hire_date) BETWEEN TO_DATE(:startDate, 'YYYY-MM-DD') AND TO_DATE(:endDate, 'YYYY-MM-DD')"
  ```

Java check item 6: In SQL string literals, use lowercase for identifiers (like table and column names) and data type (like varchar), use uppercase for SQL keywords (like SELECT, FROM, WHERE).
  ```java
  // Before migration (Oracle)
  String sql = """
          INSERT INTO EMPLOYEES (
              EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL,
              PHONE_NUMBER, HIRE_DATE, JOB_ID, SALARY,
              COMMISSION_PCT, MANAGER_ID, DEPARTMENT_ID
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      """;

  // After migration (PostgreSQL)
  String sql = """
          INSERT INTO employees (
              employee_id, first_name, last_name, email,
              phone_number, hire_date, job_id, salary,
              commission_pct, manager_id, department_id
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      """;
  ```

Java check item 7: Replace PL/SQL BULK COLLECT and FORALL with standard JDBC batch operations.
  ```java
  // Before migration (Oracle)
  String plsql = """
          DECLARE
              TYPE emp_id_array IS TABLE OF EMPLOYEES.EMPLOYEE_ID%TYPE;
              TYPE salary_array IS TABLE OF EMPLOYEES.SALARY%TYPE;
              l_emp_ids emp_id_array;
              l_salaries salary_array;
              l_increase_pct NUMBER := ?;
          BEGIN
              -- Bulk collect employee IDs and salaries
              SELECT EMPLOYEE_ID, SALARY BULK COLLECT INTO l_emp_ids, l_salaries
              FROM EMPLOYEES
              WHERE EMPLOYEE_ID IN (?, ?, ?);
              -- Use FORALL to update all records in a single operation
              FORALL i IN 1..l_emp_ids.COUNT
                  UPDATE EMPLOYEES
                  SET SALARY = l_salaries(i) * (1 + l_increase_pct)
                  WHERE EMPLOYEE_ID = l_emp_ids(i);
              COMMIT;
          END;
          """;
  jdbcTemplate.update(plsql, params);

  // After migration (PostgreSQL)
  String sql = "UPDATE employees SET salary = salary * (1 + ?) WHERE employee_id = ?";
  List<Object[]> batchArgs = new ArrayList<>();
  for (Long employeeId : employeeIds) {
      batchArgs.add(new Object[] { increasePercent, employeeId });
  }
  jdbcTemplate.batchUpdate(sql, batchArgs);
  ```

Java check item 8: Replace hierarchical CONNECT BY queries with recursive CTEs.
  Example 1:
  ```java
  // Before migration (Oracle)
  String sql = """
          SELECT
              LEVEL as hierarchy_level,
              LPAD(' ', (LEVEL-1)*2, ' ') || e.FIRST_NAME || ' ' || e.LAST_NAME as employee_name,
              e.EMPLOYEE_ID,
              e.JOB_ID,
              e.SALARY,
              e.DEPARTMENT_ID
          FROM
              EMPLOYEES e
          START WITH
              e.EMPLOYEE_ID = ?
          CONNECT BY
              e.MANAGER_ID = PRIOR e.EMPLOYEE_ID
          ORDER SIBLINGS BY
              e.FIRST_NAME, e.LAST_NAME
      """;

  // After migration (PostgreSQL)
  String sql = """
          WITH RECURSIVE emp_hierarchy AS (
              -- Base case: start with the specific employee
              SELECT
                  e.employee_id,
                  e.first_name,
                  e.last_name,
                  e.job_id,
                  e.salary,
                  e.department_id,
                  e.manager_id,
                  1 as hierarchy_level
              FROM employees e
              WHERE e.employee_id = ?

              UNION ALL

              -- Recursive case: find the subordinates of the current employee
              SELECT
                  m.employee_id,
                  m.first_name,
                  m.last_name,
                  m.job_id,
                  m.salary,
                  m.department_id,
                  m.manager_id,
                  eh.hierarchy_level + 1
              FROM employees m
              JOIN emp_hierarchy eh ON m.manager_id = eh.employee_id
          )
          SELECT
              hierarchy_level,
              LPAD(' ', (hierarchy_level-1)*2, ' ') || first_name || ' ' || last_name as employee_name,
              employee_id,
              job_id,
              salary,
              department_id
          FROM emp_hierarchy
          ORDER BY hierarchy_level, first_name, last_name
          """;
  ```

  Example 2:
  ```java
  // Before migration (Oracle)
  String sql = """
              SELECT
                  e.EMPLOYEE_ID,
                  e.FIRST_NAME || ' ' || e.LAST_NAME as employee_name,
                  SYS_CONNECT_BY_PATH(e.FIRST_NAME || ' ' || e.LAST_NAME, ' -> ') as hierarchy_path,
                  CONNECT_BY_ROOT (e.FIRST_NAME || ' ' || e.LAST_NAME) as top_manager,
                  LEVEL as hierarchy_level,
                  CONNECT_BY_ISLEAF as is_leaf
              FROM
                  EMPLOYEES e
              START WITH
                  e.EMPLOYEE_ID = ?
              CONNECT BY
                  e.EMPLOYEE_ID = PRIOR e.MANAGER_ID
              ORDER BY hierarchy_level
          """;

  // After migration (PostgreSQL)
  // Important: "RECURSIVE" in the SQL is necessary.
  String sql = """
          WITH RECURSIVE emp_hierarchy(employee_id, first_name, last_name, manager_id, level_num) AS (
              SELECT employee_id, first_name, last_name, manager_id, 1
              FROM employees
              WHERE employee_id = ?
              UNION ALL
              SELECT e.employee_id, e.first_name, e.last_name, e.manager_id, eh.level_num + 1
              FROM employees e JOIN emp_hierarchy eh ON e.employee_id = eh.manager_id
          )
          SELECT
              employee_id,
              first_name,
              last_name,
              manager_id,
              level_num
          FROM emp_hierarchy
          ORDER BY level_num
      """;
  ```

Java check item 9: Replace MODEL clause with CTEs and UNION ALL queries.
  ```java
  // Before migration (Oracle)
  String sql = """
          SELECT
              DEPARTMENT_ID,
              EMPLOYEE_ID,
              LAST_NAME,
              YEAR,
              PROJECTED_SALARY
          FROM (
               SELECT
                  DEPARTMENT_ID,
                  EMPLOYEE_ID,
                  LAST_NAME,
                  SALARY
              FROM EMPLOYEES
              WHERE DEPARTMENT_ID IS NOT NULL
          )
          MODEL
              PARTITION BY (DEPARTMENT_ID)
              DIMENSION BY (EMPLOYEE_ID, 0 AS YEAR)
              MEASURES (LAST_NAME, SALARY AS PROJECTED_SALARY)
              RULES (
                  PROJECTED_SALARY[FOR EMPLOYEE_ID IN (SELECT EMPLOYEE_ID FROM EMPLOYEES WHERE DEPARTMENT_ID IS NOT NULL), 1] =
                      PROJECTED_SALARY[CV(), 0] * 1.05,
                  PROJECTED_SALARY[FOR EMPLOYEE_ID IN (SELECT EMPLOYEE_ID FROM EMPLOYEES WHERE DEPARTMENT_ID IS NOT NULL), 2] =
                      PROJECTED_SALARY[CV(), 1] * 1.05,
                  PROJECTED_SALARY[FOR EMPLOYEE_ID IN (SELECT EMPLOYEE_ID FROM EMPLOYEES WHERE DEPARTMENT_ID IS NOT NULL), 3] =
                      PROJECTED_SALARY[CV(), 2] * 1.05
              )
          ORDER BY DEPARTMENT_ID, EMPLOYEE_ID, YEAR
      """;

  // After migration (PostgreSQL)
  String sql = """
          WITH base_data AS (
               SELECT
                  department_id,
                  employee_id,
                  last_name,
                  salary
              FROM employees
              WHERE department_id IS NOT NULL
          )
          SELECT
              department_id,
              employee_id,
              last_name,
              0 AS year,
              salary AS projected_salary
          FROM base_data

          UNION ALL

          SELECT
              department_id,
              employee_id,
              last_name,
              1 AS year,
              salary * 1.05 AS projected_salary
          FROM base_data

          UNION ALL

          SELECT
              department_id,
              employee_id,
              last_name,
              2 AS year,
              salary * 1.05 * 1.05 AS projected_salary
          FROM base_data

          UNION ALL

          SELECT
              department_id,
              employee_id,
              last_name,
              3 AS year,
              salary * 1.05 * 1.05 * 1.05 AS projected_salary
          FROM base_data

          ORDER BY department_id, employee_id, year
      """;
  ```

Java check item 10: Replace PIVOT clause with CASE-based conditional aggregations.
  ```java
  // Before migration (Oracle)
  String sql = """
          SELECT * FROM (
              SELECT DEPARTMENT_ID, JOB_ID
              FROM EMPLOYEES
              WHERE DEPARTMENT_ID IS NOT NULL
          )
          PIVOT (
              COUNT(*)
              FOR JOB_ID IN (
                  'IT_PROG' AS IT_PROGRAMMERS,
                  'SA_REP' AS SALES_REPS,
                  'FI_ACCOUNT' AS ACCOUNTANTS,
                  'SA_MAN' AS SALES_MANAGERS
              )
          )
          ORDER BY DEPARTMENT_ID
      """;

  // After migration (PostgreSQL)
  String sql = """
          SELECT
              department_id,
              COUNT(CASE WHEN job_id = 'IT_PROG' THEN 1 END) AS it_programmers,
              COUNT(CASE WHEN job_id = 'SA_REP' THEN 1 END) AS sales_reps,
              COUNT(CASE WHEN job_id = 'FI_ACCOUNT' THEN 1 END) AS accountants,
              COUNT(CASE WHEN job_id = 'SA_MAN' THEN 1 END) AS sales_managers
          FROM
              employees
          WHERE
              department_id IS NOT NULL
          GROUP BY
              department_id
          ORDER BY
              department_id
      """;
  ```

Java check item 11: Replace PIVOT clause with CASE expressions for category counts.
  ```java
  // Before migration (Oracle)
  String sql = """
      SELECT * FROM (
          SELECT DEPARTMENT_ID, CATEGORY_ID
          FROM ITEMS
          WHERE DEPARTMENT_ID IS NOT NULL
      )
      PIVOT (
          COUNT(*)
          FOR CATEGORY_ID IN (
              'TYPE_1' AS TYPE1_COUNT,
              'TYPE_2' AS TYPE2_COUNT,
              'TYPE_3' AS TYPE3_COUNT,
              'TYPE_4' AS TYPE4_COUNT
          )
      )
      ORDER BY DEPARTMENT_ID
  """;

  // After migration (PostgreSQL)
  String sql = """
      SELECT
          department_id,
          COUNT(CASE WHEN category_id = 'TYPE_1' THEN 1 END) AS type1_count,
          COUNT(CASE WHEN category_id = 'TYPE_2' THEN 1 END) AS type2_count,
          COUNT(CASE WHEN category_id = 'TYPE_3' THEN 1 END) AS type3_count,
          COUNT(CASE WHEN category_id = 'TYPE_4' THEN 1 END) AS type4_count
      FROM
          items
      WHERE
          department_id IS NOT NULL
      GROUP BY
          department_id
      ORDER BY
          department_id
  """;
  ```

Java check item 12: Remove schema and package references from SimpleJdbcCall procedures.
  ```java
  // Before migration (Oracle)
  SimpleJdbcCall jdbcCall = new SimpleJdbcCall(dataSource)
          .withSchemaName("TEST")
          .withCatalogName("HR")      // Package name
          .withProcedureName("GET_EMPLOYEE_INFO")
          .declareParameters(
                  new org.springframework.jdbc.core.SqlParameter("p_employee_id", Types.NUMERIC),
                  new org.springframework.jdbc.core.SqlOutParameter("p_result", Types.REF_CURSOR)
          );

  // After migration (PostgreSQL)
  SimpleJdbcCall jdbcCall = new SimpleJdbcCall(jdbcTemplate)
          .withProcedureName("get_employee_info")
          .declareParameters(
                  new org.springframework.jdbc.core.SqlParameter("p_employee_id", Types.NUMERIC),
                  new org.springframework.jdbc.core.SqlOutParameter("p_result", Types.REF_CURSOR)
          );
  ```

Java check item 13: Replace OracleContainer with PostgreSQLContainer in test classes.
  ```java
  // Before migration (Oracle)
  import org.testcontainers.containers.OracleContainer;

  @Testcontainers
  public abstract class AbstractTestBase {
      private static final String ORACLE_IMAGE = "gvenzl/oracle-xe:latest";

      @Container
      protected static final OracleContainer oracleContainer = new OracleContainer(ORACLE_IMAGE)
              .withUsername("test")
              .withPassword("test");

      @DynamicPropertySource
      static void registerOracleProperties(DynamicPropertyRegistry registry) {
          registry.add("spring.datasource.url", oracleContainer::getJdbcUrl);
          registry.add("spring.datasource.username", oracleContainer::getUsername);
          registry.add("spring.datasource.password", oracleContainer::getPassword);
          registry.add("spring.datasource.driver-class-name", () -> "oracle.jdbc.OracleDriver");
      }
  }

  // After migration (PostgreSQL)
  import org.testcontainers.containers.PostgreSQLContainer;

  @Testcontainers
  public abstract class AbstractTestBase {
      private static final String POSTGRES_IMAGE = "postgres:latest";

      @Container
      protected static final PostgreSQLContainer<?> postgresContainer =
          new PostgreSQLContainer<>(POSTGRES_IMAGE)
              .withUsername("test")
              .withPassword("test")
              .withDatabaseName("testdb");

      @DynamicPropertySource
      static void registerPostgresProperties(DynamicPropertyRegistry registry) {
          registry.add("spring.datasource.url", postgresContainer::getJdbcUrl);
          registry.add("spring.datasource.username", postgresContainer::getUsername);
          registry.add("spring.datasource.password", postgresContainer::getPassword);
          registry.add("spring.datasource.driver-class-name", () -> "org.postgresql.Driver");
      }
  }
  ```

Java check item 14: Update SQL script parsers to support dollar-quoted strings and PL/pgSQL syntax.
  ```java
  // Before migration (Oracle - parsing PL/SQL blocks)
  public String[] splitScriptIntoStatements(String script) {
      List<String> statements = new ArrayList<>();
      StringBuilder currentStatement = new StringBuilder();
      boolean inPlSqlBlock = false;

      for (String line : script.split("\n")) {
          if (line.trim().isEmpty() || line.trim().startsWith("--")) {
              continue;
          }

          // Check for standalone slash indicating end of PL/SQL block
          if (line.trim().equals("/")) {
              if (inPlSqlBlock) {
                  statements.add(currentStatement.toString().trim());
                  currentStatement = new StringBuilder();
                  inPlSqlBlock = false;
              }
              continue;
          }

          // Check for potential start of PL/SQL block
          if (!inPlSqlBlock &&
              (line.toUpperCase().contains("CREATE OR REPLACE PROCEDURE") ||
               line.toUpperCase().contains("CREATE OR REPLACE PACKAGE"))) {
              inPlSqlBlock = true;
          }

          currentStatement.append(line).append("\n");

          if (!inPlSqlBlock && line.trim().endsWith(";")) {
              statements.add(currentStatement.toString().trim());
              currentStatement = new StringBuilder();
          }
      }

      return statements.toArray(new String[0]);
  }

  // After migration (PostgreSQL - supporting dollar-quoted strings)
  public String[] splitScriptIntoStatements(String script) {
      List<String> statements = new ArrayList<>();
      StringBuilder currentStatement = new StringBuilder();
      boolean inPlSqlBlock = false;
      boolean inDollarQuotedString = false;
      boolean collectingProcedureOrFunction = false;

      for (String line : script.split("\n")) {
          if (line.trim().isEmpty() || line.trim().startsWith("--")) {
              continue;
          }

          // Check for PostgreSQL style functions with $$ delimiter
          if (!inPlSqlBlock && !collectingProcedureOrFunction &&
              (line.toUpperCase().contains("CREATE OR REPLACE PROCEDURE") ||
               line.toUpperCase().contains("CREATE OR REPLACE FUNCTION"))) {
              collectingProcedureOrFunction = true;
          }

          // Check for dollar quoted string - PostgreSQL syntax
          if (line.contains("$$")) {
              if (collectingProcedureOrFunction && !inPlSqlBlock) {
                  inPlSqlBlock = true;
              }
              inDollarQuotedString = !inDollarQuotedString;
          }

          // Special handling for the end of PostgreSQL function/procedure
          if (collectingProcedureOrFunction &&
              line.toUpperCase().contains("LANGUAGE PLPGSQL") &&
              !inDollarQuotedString) {
              inPlSqlBlock = false;
              collectingProcedureOrFunction = false;
          }

          currentStatement.append(line).append("\n");

          if (!inPlSqlBlock && !collectingProcedureOrFunction &&
              line.trim().endsWith(";")) {
              statements.add(currentStatement.toString().trim());
              currentStatement = new StringBuilder();
          }
      }

      return statements.toArray(new String[0]);
  }
  ```

Java check item 15: Replace multi-statement PL/SQL blocks with individual SQL statements.
  ```java
  // Before migration (Oracle)
  String plsqlBlock = """
          BEGIN
            UPDATE EMPLOYEES
            SET SALARY = SALARY + ?
            WHERE EMPLOYEE_ID = ?;

            INSERT INTO SALARY_HISTORY (
              EMPLOYEE_ID,
              CHANGE_DATE,
              SALARY_CHANGE,
              CHANGE_REASON
            ) VALUES (
              ?,
              SYSDATE,
              ?,
              'Annual increase'
            );

            COMMIT;
          EXCEPTION
            WHEN OTHERS THEN
              ROLLBACK;
              RAISE;
          END;
          """;

  jdbcTemplate.update(plsqlBlock,
          salaryIncrease,
          employeeId,
          employeeId,
          salaryIncrease);

  // After migration (PostgreSQL)
  // Execute statements individually
  jdbcTemplate.update(
          "UPDATE employees SET salary = salary + ? WHERE employee_id = ?",
          salaryIncrease, employeeId
  );

  jdbcTemplate.update(
          "INSERT INTO salary_history (employee_id, change_date, salary_change, change_reason) " +
          "VALUES (?, CURRENT_DATE, ?, 'Annual increase')",
          employeeId, salaryIncrease
  );
  ```

Java check item 16: Replace SimpleJdbcCall with CALL syntax for PostgreSQL procedures. Add type cast in parameter if necessary.
  Before migration (Oracle)
  ```sql
  CREATE TABLE EMPLOYEES (
      EMPLOYEE_ID     NUMBER(6) PRIMARY KEY, -- Caution about the type here
      SALARY          NUMBER(8,2)
  );
  CREATE OR REPLACE PROCEDURE update_employee_salary( -- This is the definition of the stored procedure
      p_employee_id IN EMPLOYEES.EMPLOYEE_ID%TYPE, -- Caution about the type here
      p_percent IN NUMBER
  ) IS
  BEGIN
      UPDATE EMPLOYEES
      SET SALARY = SALARY * (1 + p_percent/100)
      WHERE EMPLOYEE_ID = p_employee_id;
      COMMIT;
  EXCEPTION
      WHEN OTHERS THEN
          ROLLBACK;
          RAISE;
  END update_employee_salary;
  /
  ```
  ```java
  // Using SimpleJdbcCall to call Oracle stored procedure
  SimpleJdbcCall jdbcCall = new SimpleJdbcCall(jdbcTemplate)
          .withProcedureName("update_employee_salary");

  Map<String, Object> inParams = new HashMap<>();
  inParams.put("p_employee_id", employeeId);
  inParams.put("p_percent", percentIncrease);

  jdbcCall.execute(inParams);
  ```

  After migration (PostgreSQL)
  ```sql
  CREATE TABLE employees (
      employee_id     integer PRIMARY KEY, -- Caution about the type here
      salary          numeric(8,2)
  );
  CREATE OR REPLACE PROCEDURE update_employee_salary( -- This is the definition of the stored procedure
      p_employee_id integer, -- Caution about the type here
      p_percent numeric
  ) AS $$
  BEGIN
      UPDATE employees
      SET salary = salary * (1 + p_percent/100)
      WHERE employee_id = p_employee_id;
  END;
  $$ LANGUAGE plpgsql;
  ```
  ```java
  // In PostgreSQL, procedures are called with CALL syntax
  String sql = "CALL update_employee_salary(CAST(? AS INTEGER), CAST(? AS NUMERIC))"; // Caution about the type cast here, it depends on the definition of the stored procedure
  jdbcTemplate.update(sql, employeeId, percentIncrease);
  ```

Java check item 17: Replace ROWNUM pagination with LIMIT/OFFSET in native SQL queries.
  ```java
  // Before migration (Oracle)
  @Query(value = "SELECT * FROM (SELECT a.*, ROWNUM rn FROM " +
          "(SELECT * FROM ITEMS ORDER BY PRICE DESC) a " +
          "WHERE ROWNUM <= :maxResults) WHERE rn >= :startIndex", nativeQuery = true)
  List<Item> findItemsWithPagination(@Param("startIndex") int startIndex,
                                    @Param("maxResults") int maxResults);

  // After migration (PostgreSQL)
  @Query(value = "SELECT * FROM items ORDER BY price DESC " +
          "LIMIT :maxResults OFFSET :startIndex - 1", nativeQuery = true)
  List<Item> findItemsWithPagination(@Param("startIndex") int startIndex,
                                    @Param("maxResults") int maxResults);
  ```

Java check item 18: Replace SYS_CONNECT_BY_PATH with string concatenation in recursive CTEs.
  ```java
  // Before migration (Oracle)
  String sql = """
      SELECT
          i.ITEM_ID,
          i.NAME as item_name,
          SYS_CONNECT_BY_PATH(i.NAME, ' -> ') as hierarchy_path,
          CONNECT_BY_ROOT (i.NAME) as top_item,
          LEVEL as hierarchy_level,
          CONNECT_BY_ISLEAF as is_leaf
      FROM
          ITEMS i
      START WITH
          i.ITEM_ID = ?
      CONNECT BY
          i.ITEM_ID = PRIOR i.PARENT_ID
      ORDER BY hierarchy_level
  """;
  // After migration (PostgreSQL)
  String sql = """
      WITH RECURSIVE item_hierarchy AS (
          -- Base case
          SELECT
              i.item_id,
              i.name as item_name,
              i.name as hierarchy_path,
              1 as hierarchy_level
          FROM
              items i
          WHERE
              i.item_id = ?

          UNION ALL

          -- Recursive case
          SELECT
              i.item_id,
              i.name,
              ih.hierarchy_path || ' -> ' || i.name,
              ih.hierarchy_level + 1
          FROM
              items i
          JOIN
              item_hierarchy ih ON i.parent_id = ih.item_id
      )
      SELECT
          item_id,
          item_name,
          hierarchy_path,
          hierarchy_level,
          (NOT EXISTS (
              SELECT 1 FROM items
              WHERE parent_id = item_hierarchy.item_id
          )) as is_leaf
      FROM
          item_hierarchy
      ORDER BY
          hierarchy_level
  """;
  ```

Java check item 19: Replace MEDIAN with PERCENTILE_CONT(0.5) WITHIN GROUP in SQL queries.
  ```java
  // Before migration (Oracle)
  String sql = """
      SELECT
          DEPARTMENT_ID,
          AVG(SALARY) AS AVG_SALARY,
          MIN(SALARY) AS MIN_SALARY,
          MAX(SALARY) AS MAX_SALARY,
          COUNT(*) AS EMP_COUNT,
          MEDIAN(SALARY) AS MEDIAN_SALARY
      FROM ITEMS
      GROUP BY DEPARTMENT_ID
      ORDER BY DEPARTMENT_ID
  """;

  // After migration (PostgreSQL)
  String sql = """
      SELECT
          department_id,
          AVG(value) AS avg_value,
          MIN(value) AS min_value,
          MAX(value) AS max_value,
          COUNT(*) AS item_count,
          PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value) AS median_value
      FROM items
      GROUP BY department_id
      ORDER BY department_id
  """;
  ```

Java check item 20: Use executeFunction() for stored function calls in SimpleJdbcCall.
  ```java
  // Before migration (Oracle)
  public BigDecimal calculateItemValue(Long itemId, BigDecimal percentage) {
      SimpleJdbcCall jdbcCall = new SimpleJdbcCall(dataSource)
              .withSchemaName("TEST")
              .withCatalogName("ITEMS_PKG")
              .withFunctionName("CALCULATE_VALUE")
              .declareParameters(
                      new SqlParameter("p_item_id", Types.NUMERIC),
                      new SqlParameter("p_percent", Types.NUMERIC),
                      new SqlOutParameter("return", Types.NUMERIC)
              );

      SqlParameterSource params = new MapSqlParameterSource()
              .addValue("p_item_id", itemId)
              .addValue("p_percent", percentage);

      Map<String, Object> result = jdbcCall.execute(params);
      return (BigDecimal) result.get("return");
  }

  // After migration (PostgreSQL)
  public BigDecimal calculateItemValue(Long itemId, BigDecimal percentage) {
      SimpleJdbcCall jdbcCall = new SimpleJdbcCall(jdbcTemplate)
              .withFunctionName("calculate_value")
              .declareParameters(
                      new SqlParameter("p_item_id", Types.NUMERIC),
                      new SqlParameter("p_percent", Types.NUMERIC)
              );

      SqlParameterSource params = new MapSqlParameterSource()
              .addValue("p_item_id", itemId)
              .addValue("p_percent", percentage);

      return jdbcCall.executeFunction(BigDecimal.class, params);
  }
  ```

Java check item 21: Remove "FROM dual" in function call SQL statements.
  ```java
  // Before migration (Oracle)
  BigDecimal result = jdbcTemplate.queryForObject(
      "SELECT calculate_compensation(?, ?) FROM dual",
      BigDecimal.class,
      salary,
      commissionPct
  );

  // After migration (PostgreSQL)
  BigDecimal result = jdbcTemplate.queryForObject(
      "SELECT calculate_compensation(?, ?)",
      BigDecimal.class,
      salary,
      commissionPct
  );
  ```

Java check item 22: Add explicit type casting (::) for column and function parameters in SQL according to function definition. Because PostgreSQL is more strict about parameter types in stored procedure calls.
  Example one: In function parameter.
      Before migration (Oracle)
      ```sql
      FUNCTION CALCULATE_BONUS(
          p_employee_id IN NUMBER,
          p_percent IN NUMBER
      ) RETURN NUMBER IS
          v_salary EMPLOYEES.SALARY%TYPE;
          v_bonus NUMBER;
      BEGIN
          SELECT SALARY INTO v_salary FROM EMPLOYEES WHERE EMPLOYEE_ID = p_employee_id;
          v_bonus := v_salary * (p_percent / 100);
          RETURN v_bonus;
      END CALCULATE_BONUS;
      ```
      ```java
      BigDecimal bonus = jdbcTemplate.queryForObject(
          "SELECT calculate_bonus(?, ?)",
          BigDecimal.class,
          itemId,
          percent
      );

      After migration (PostgreSQL)
      ```sql
      CREATE OR REPLACE FUNCTION calculate_bonus(
          p_employee_id INTEGER,
          p_percent INTEGER
      ) RETURNS NUMERIC AS $$
      DECLARE
          v_salary employees.salary%TYPE;
          v_bonus NUMERIC;
      BEGIN
          SELECT salary INTO v_salary FROM employees WHERE employee_id = p_employee_id;
          -- Use numeric division to avoid integer division truncation
          v_bonus := v_salary * (p_percent::numeric / 100);
          RETURN v_bonus;
      END;
      $$ LANGUAGE plpgsql;
      ```
      ```java
      BigDecimal bonus = jdbcTemplate.queryForObject(
          "SELECT calculate_bonus(?::INTEGER, ?::INTEGER)", // Add casting  according to the function definition.
          BigDecimal.class,
          itemId,
          percent.intValue()
      );
      ```
  Example 2: In Column.
      ```java
      String sql = "SELECT last_name::varchar as emp_path FROM employees"
      ```

Java check item 23: Replace REF_CURSOR handling with direct queries or PostgreSQL's named cursors.
  ```java
  // Before migration (Oracle)
  // Use SimpleJdbcCall to call stored procedure with cursor
  SimpleJdbcCall jdbcCall = new SimpleJdbcCall(jdbcTemplate)
          .withCatalogName("HR") // Package name
          .withProcedureName("GET_ITEM_INFO")
          .declareParameters(
                  new SqlParameter("p_item_id", Types.NUMERIC),
                  new SqlOutParameter("p_result", Types.REF_CURSOR)
          );

  MapSqlParameterSource params = new MapSqlParameterSource()
          .addValue("p_item_id", itemId);
  Map<String, Object> result = jdbcCall.execute(params);

  @SuppressWarnings("unchecked")
  Map<String, Object> itemInfo = (Map<String, Object>) ((java.util.List<?>) result.get("p_result")).get(0);

  // After migration (PostgreSQL) - Option 1: Direct query approach
  Map<String, Object> itemInfo = jdbcTemplate.queryForMap(
      "SELECT i.*, c.category_name FROM items i " +
      "JOIN categories c ON i.category_id = c.category_id " +
      "WHERE i.item_id = ?",
      itemId
  );

  // After migration (PostgreSQL) - Option 2: If cursor is required
  // Create a named refcursor
  jdbcTemplate.execute("BEGIN; DECLARE c_item REFCURSOR;");

  // Call the stored procedure
  jdbcTemplate.update("CALL get_item_info(?, 'c_item')", itemId);

  // Fetch results from the cursor
  Map<String, Object> itemInfo = jdbcTemplate.queryForMap("FETCH ALL FROM c_item");

  jdbcTemplate.execute("COMMIT;");
  ```

Java check item 24: Replace MERGE statement with INSERT ON CONFLICT for upsert operations.
  ```java
  // Before migration (Oracle)
  String mergeSql =
          "MERGE INTO items i " +
          "USING (SELECT :itemId AS item_id, :itemName AS item_name, " +
          ":categoryId AS category_id FROM dual) src " +
          "ON (i.ITEM_ID = src.item_id) " +
          "WHEN MATCHED THEN " +
          "UPDATE SET i.ITEM_NAME = src.item_name, " +
          "i.CATEGORY_ID = src.category_id " +
          "WHEN NOT MATCHED THEN " +
          "INSERT (ITEM_ID, ITEM_NAME, CATEGORY_ID) " +
          "VALUES (src.item_id, src.item_name, src.category_id)";

  MapSqlParameterSource params = new MapSqlParameterSource()
          .addValue("itemId", itemId)
          .addValue("itemName", itemName)
          .addValue("categoryId", categoryId);

  int rowsAffected = jdbcTemplate.update(mergeSql, params);

  // After migration (PostgreSQL)
  String upsertSql =
          "INSERT INTO items (item_id, item_name, category_id) " +
          "VALUES (:itemId, :itemName, :categoryId) " +
          "ON CONFLICT (item_id) " +
          "DO UPDATE SET " +
          "item_name = :itemName, " +
          "category_id = :categoryId";

  MapSqlParameterSource params = new MapSqlParameterSource()
          .addValue("itemId", itemId)
          .addValue("itemName", itemName)
          .addValue("categoryId", categoryId);

  int rowsAffected = jdbcTemplate.update(upsertSql, params);
  ```

Java check item 25: Use JdbcTemplate.queryForObject to replace SimpleJdbcCall#executeFunction.
  ```java
  // Before migration (Oracle)
  SimpleJdbcCall calculateBonusCall = new SimpleJdbcCall(jdbcTemplate)
          .withCatalogName("HR") // Package name
          .withFunctionName("CALCULATE_BONUS")
          .declareParameters(
                  new SqlParameter("p_item_id", Types.NUMERIC),
                  new SqlParameter("p_percent", Types.NUMERIC)
          );

  SqlParameterSource inParams = new MapSqlParameterSource()
          .addValue("p_item_id", itemId)
          .addValue("p_percent", percent);

  BigDecimal bonus = calculateBonusCall.executeFunction(BigDecimal.class, inParams);

  // After migration (PostgreSQL)
  // In PostgreSQL, we can call functions directly with SELECT
  // Add casting if necessary according to the function definition.
  String sql = "SELECT calculate_bonus(?::INTEGER, ?::INTEGER)";
  BigDecimal bonus = jdbcTemplate.queryForObject(sql, BigDecimal.class,
          itemId, percent.intValue());
  ```

Java check item 26: Change H2 from Oracle mode to PostgreSQL mode.
  ```java
  // Before migration (Oracle)
  import org.h2.jdbcx.JdbcDataSource;

  public class OracleTestSetup {
      public static JdbcDataSource createOracleDataSource(String dbName) {
          JdbcDataSource h2DataSource = new JdbcDataSource();
          h2DataSource.setURL("jdbc:h2:mem:" + dbName + ";MODE=Oracle;DB_CLOSE_DELAY=-1");
          h2DataSource.setUser("sa");
          h2DataSource.setPassword("");
          return h2DataSource;
      }
  }

  // After migration (PostgreSQL)
  import org.h2.jdbcx.JdbcDataSource;

  public class PostgresTestSetup {
      public static JdbcDataSource createPostgresDataSource(String dbName) {
          JdbcDataSource h2DataSource = new JdbcDataSource();
          h2DataSource.setURL("jdbc:h2:mem:" + dbName + ";MODE=PostgreSQL;DB_CLOSE_DELAY=-1");
          h2DataSource.setUser("sa");
          h2DataSource.setPassword("");
          return h2DataSource;
      }
  }
  ```

Java check item 27: Change from OracleDataSource to PGSimpleDataSource.
  ```java
  // Before migration (Oracle)
  public static DataSource createOracleDataSource(String user, String password, String url) {
      OracleDataSource dataSource = null;
      try {
          dataSource = new OracleDataSource();
          dataSource.setUser(user);
          dataSource.setPassword(password);
          dataSource.setURL(url); // e.g., jdbc:oracle:thin:@localhost:1521:xe
          dataSource.setImplicitCachingEnabled(true);
          return dataSource;
      } catch (SQLException e) {
          e.printStackTrace();
      }
      return null;
  }

  // After migration (PostgreSQL)
  public static DataSource createPostgresDataSource(String user, String password, String url) {
      PGSimpleDataSource dataSource = new PGSimpleDataSource();
      try {
          dataSource.setUser(user);
          dataSource.setPassword(password);
          dataSource.setURL(url); // e.g., jdbc:postgresql://localhost:5432/mydb
          return dataSource;
      } catch (Exception e) {
          e.printStackTrace();
      }
      return null;
  }
  ```

Java check item 28: Enable passwordless connection. comment out all "username" and "password" related content which are ONLY corresponding to the PostgreSQL JDBC URL.
- Example: Java code difference fragment 1
  ```diff
  - @Value("${spring.shardingsphere.dataSource1.username}")
  - private String username;
  - @Value("${spring.shardingsphere.dataSource1.password}")
  - private String password;
  + // Comment out all content about "username" and "password" because now PostgreSQL will authenticate using managed identity.
  + // @Value("${spring.shardingsphere.dataSource1.username}")
  + // private String username;
  + // @Value("${spring.shardingsphere.dataSource1.password}")
  + // private String password;
  ```
- Example: Java code difference fragment 2
  ```diff
  - hikariDataSource.setUsername(dataSource1Config.getUsername());
  - hikariDataSource.setPassword(dataSource1Config.getPassword());
  + // Comment out all content about "username" and "password" because now PostgreSQL will authenticate using managed identity.
  + // hikariDataSource.setUsername(dataSource1Config.getUsername());
  + // hikariDataSource.setPassword(dataSource1Config.getPassword());
  ```

Java check item 9999: Migrate all other Oracle-specific content to PostgreSQL. For each line, carefully verify whether it uses Oracle-only features.
