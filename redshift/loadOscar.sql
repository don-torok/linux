#copy dtorok.mdcr_1p_oscar_results
#(source_table_name
#, statistic_type
#, statistic_value
#, summary_level
#, variable_description_level_1
#, variable_description_level_2
#, variable_description_level_3
#, variable_name
#, variable_type
#, variable_value
#, variable_value_level_1
#, variable_value_level_2
#, variable_value_level_3)
#FROM 's3://dtk-transfer/oscar/mdcr_1p_oscar.txt'
#credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
#removeQuotes  trimBlanks emptyAsNull blanksasnull IGNOREHEADER 1
#;
#copy dtorok.mdcr_1p_oscar_results_sql
#FROM 's3://dtk-transfer/oscar/person_oscar.csv'
#credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
#removeQuotes  trimBlanks emptyAsNull blanksasnull
#;
#copy dtorok.mdcr_1p_oscar_results_sql
#FROM 's3://dtk-transfer/oscar/drug_exposure_20140612.txt'
#credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
#removeQuotes  trimBlanks emptyAsNull blanksasnull
#;
#copy dtorok.mdcr_1p_oscar_results_sql
#FROM 's3://dtk-transfer/oscar/drug_era.csv'
#credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
#removeQuotes  trimBlanks emptyAsNull blanksasnull
#;
#copy dtorok.mdcr_1p_oscar_results_sql
#FROM 's3://dtk-transfer/oscar/condition_occurrence_20140612.txt'
#credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
#removeQuotes  trimBlanks emptyAsNull blanksasnull
#;
copy dtorok.mdcr_1p_oscar_results_sql
FROM 's3://dtk-transfer/oscar/condition_era_oscar.csv'
credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
removeQuotes  trimBlanks emptyAsNull blanksasnull
;
copy dtorok.mdcr_1p_oscar_results_sql
FROM 's3://dtk-transfer/oscar/death_oscar.csv'
credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
removeQuotes  trimBlanks emptyAsNull blanksasnull
;
copy dtorok.mdcr_1p_oscar_results_sql
FROM 's3://dtk-transfer/oscar/drug_cost_oscar.csv'
credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
removeQuotes  trimBlanks emptyAsNull blanksasnull
;
copy dtorok.mdcr_1p_oscar_results_sql
FROM 's3://dtk-transfer/oscar/observation_oscar.csv'
credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
removeQuotes  trimBlanks emptyAsNull blanksasnull
;
copy dtorok.mdcr_1p_oscar_results_sql
FROM 's3://dtk-transfer/oscar/observation_period_oscar.csv'
credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
removeQuotes  trimBlanks emptyAsNull blanksasnull
;
copy dtorok.mdcr_1p_oscar_results_sql
FROM 's3://dtk-transfer/oscar/procedure_cost_oscar.csv'
credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
removeQuotes  trimBlanks emptyAsNull blanksasnull
;
copy dtorok.mdcr_1p_oscar_results_sql
FROM 's3://dtk-transfer/oscar/procedure_occurrence_oscar.csv'
credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
removeQuotes  trimBlanks emptyAsNull blanksasnull
;
copy dtorok.mdcr_1p_oscar_results_sql
FROM 's3://dtk-transfer/oscar/provider_oscar.csv'
credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
removeQuotes  trimBlanks emptyAsNull blanksasnull
;
copy dtorok.mdcr_1p_oscar_results_sql
FROM 's3://dtk-transfer/oscar/visit_occurrence_oscar.csv'
credentials 'aws_access_key_id=XXXXXXXXXXXXXXXXXXXXXX;aws_secret_access_key=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
removeQuotes  trimBlanks emptyAsNull blanksasnull
;
