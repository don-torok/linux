#CREATE TABLE premier_1p.medRec_lookup_2 
#AS
#SELECT medrec_key
#  FROM premier_1p.medRec_lookup
# WHERE random() < 0.001
#;

#Commit;

#select count(*) from premier_1p.medRec_lookup_2;

#INSERT INTO premier_1p.pat_lookup
#SELECT distinct src.pat_key, src.medRec_key
#FROM premier_src.pat_seq src
#JOIN premier_1p.medRec_lookup_2 ON lookup.medRec_key = src.medRec_key;
#COMMIT;

#SELECT count(*) from premier_1p.pat_lookup;


#DROP TABLE premier_1p.pat_seq ;
#COMMIT;

CREATE TABLE premier_1p.pat_seq 
AS
SELECT pat_seq.* 
   FROM premier_src.pat_seq
   JOIN premier_1p.pat_lookup lookup ON lookup.pat_key = pat_seq.pat_key;
COMMIT;

DELETE FROM premier_1p.patbill;
COMMIT;

INSERT INTO premier_1p.patbill
SELECT patbill.*
  FROM premier_src.patbill
  JOIN premier_1p.pat_lookup lookup ON lookup.pat_key = patBill.pat_key;
COMMIT;

DELETE FROM premier_1p.patCPT;
COMMIT;

INSERT INTO premier_1p.patCPT
SELECT patCPT.* 
  FROM premier_src.patcpt
  JOIN premier_1p.pat_lookup lookup ON lookup.pat_key = patCPT.pat_key;
COMMIT;

DELETE FROM premier_1p.patICD;
COMMIT;

INSERT INTO premier_1p.patICD
SELECT patICD.* 
  FROM premier_src.patICD
  JOIN premier_1p.pat_lookup lookup ON lookup.pat_key = patICD.pat_key;
COMMIT;

DELETE FROM premier_1p.ss_res;
COMMIT;

INSERT
 INTO premier_1p.ss_res
SELECT ss_res.* from premier_src.ss_res
  JOIN premier_1p.pat_lookup lookup ON lookup.pat_key = ss_res.patient_key;
COMMIT;

DELETE FROM premier_1p.ss_sens;
COMMIT;

INSERT INTO premier_1p.ss_sens
SELECT ss_sens.* from premier_src.ss_sens
  JOIN premier_1p.pat_lookup lookup ON lookup.pat_key = ss_sens.patient_key;
COMMIT;


