CREATE table mdcr_cdm4_1p.visit_occurrence
AS SELECT imeds.*
FROM mdcr_cdm4.visit_occurrence imeds
JOIN mdcr_cdm4_1p.person p ON p.person_id = imeds.person_id;
analyze mdcr_cdm4_1p.visit_occurrence;


CREATE table mdcr_cdm4_1p.observation_period
AS SELECT imeds.*
FROM mdcr_cdm4.observation_period   imeds
JOIN mdcr_cdm4_1p.person  p ON p.person_id = imeds.person_id;
analyze mdcr_cdm4_1p.observation_period  ;

CREATE table mdcr_cdm4_1p.condition_era
AS SELECT imeds.*
FROM mdcr_cdm4.condition_era   imeds
JOIN mdcr_cdm4_1p.person  p ON p.person_id = imeds.person_id;
analyze mdcr_cdm4_1p.condition_era  ;

CREATE table mdcr_cdm4_1p.condition_occurrence
AS SELECT imeds.*
FROM mdcr_cdm4.condition_occurrence   imeds
JOIN mdcr_cdm4_1p.person  p ON p.person_id = imeds.person_id;
analyze  mdcr_cdm4_1p.condition_occurrence ;

CREATE table mdcr_cdm4_1p.procedure_occurrence
AS SELECT imeds.*
FROM mdcr_cdm4.procedure_occurrence   imeds
JOIN mdcr_cdm4_1p.person  p ON p.person_id = imeds.person_id;
analyze  mdcr_cdm4_1p.procedure_occurrence ;

CREATE table mdcr_cdm4_1p.procedure_cost
AS SELECT cost.*
FROM mdcr_cdm4.procedure_cost   cost
JOIN mdcr_cdm4_1p.procedure_occurrence  occur ON occur.procedure_occurrence_id = cost.procedure_occurrence_id;
analyze  mdcr_cdm4_1p.procedure_cost ;

CREATE table mdcr_cdm4_1p.observation
AS SELECT imeds.*
FROM mdcr_cdm4.observation   imeds
JOIN mdcr_cdm4_1p.person  p ON p.person_id = imeds.person_id;
analyze mdcr_cdm4_1p.observation  ;

CREATE table mdcr_cdm4_1p.payer_plan_period
AS SELECT imeds.*
FROM mdcr_cdm4.payer_plan_period   imeds
JOIN mdcr_cdm4_1p.person  p ON p.person_id = imeds.person_id;
analyze mdcr_cdm4_1p.payer_plan_period  ;

CREATE table mdcr_cdm4_1p.death
AS SELECT imeds.*
FROM mdcr_cdm4.death   imeds
JOIN mdcr_cdm4_1p.person  p ON p.person_id = imeds.person_id;
analyze mdcr_cdm4_1p.death  ;

CREATE table mdcr_cdm4_1p.drug_exposure
AS SELECT imeds.*
FROM mdcr_cdm4.drug_exposure   imeds
JOIN mdcr_cdm4_1p.person  p ON p.person_id = imeds.person_id;
analyze mdcr_cdm4_1p.drug_exposure  ;

CREATE table mdcr_cdm4_1p.drug_cost
AS SELECT cost.*
FROM mdcr_cdm4.drug_cost   cost
JOIN mdcr_cdm4_1p.drug_exposure  drug ON drug.drug_exposure_id = cost.drug_exposure_id;
analyze mdcr_cdm4_1p.drug_cost  ;

CREATE table mdcr_cdm4_1p.drug_era
AS SELECT imeds.*
FROM mdcr_cdm4.drug_era   imeds
JOIN mdcr_cdm4_1p.person  p ON p.person_id = imeds.person_id;
analyze mdcr_cdm4_1p.drug_era  ;

CREATE table mdcr_cdm4_1p.provider 
AS
SELECT *
FROM mdcr_cdm4.provider;
analyze mdcr_cdm4_1p.provider;

CREATE table mdcr_cdm4_1p.care_site
AS
SELECT *
FROM mdcr_cdm4.care_site;
analyze mdcr_cdm4_1p.care_site;

CREATE table mdcr_cdm4_1p.organization
AS
SELECT *
FROM mdcr_cdm4.organization;
analyze mdcr_cdm4_1p.organization;

CREATE table mdcr_cdm4_1p.location
AS
SELECT *
FROM mdcr_cdm4.location;
analyze mdcr_cdm4_1p.location;
