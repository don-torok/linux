UPDATE ccae_cdm4_2006_2012.drug_era
   SET drug_exposure_count 
     = ( SELECT count(*) 
           FROM public.drug_ingredient AS map 
           JOIN ccae_cdm4_2006_2012.drug_exposure AS exp 
             ON exp.drug_concept_id = map.drug_concept_id 
          WHERE drug_era.drug_concept_id = map.ingredient_concept_id 
            AND drug_era.person_id = exp.person_id 
            AND drug_exposure_start_date BETWEEN drug_era_start_date 
                                             AND drug_era_end_date 
        )
^
commit
^
select * 
from ccae_cdm4_2006_2012.drug_era
WHERE person_id = 29761698901
^
