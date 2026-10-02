import numpy as np
import pandas as pd
import pytest
from quality import assess, psi
def frame():
    return pd.DataFrame({'claim_id':['a','a','c','d'], 'patient_id':['x','y',None,'z'], 'service_date':['2026-01-01','bad','2026-01-02','2026-01-03'], 'amount':[10,-4,'oops',12], 'provider':['p']*4})
def test_known_issues_detected_without_mutation():
    df=frame(); original=df.copy(deep=True)
    issues,report=assess(df)
    assert report['checks']['duplicate_claim_id']==2
    assert report['checks']['negative_amount']==1
    assert report['checks']['invalid_amount']==1
    assert report['checks']['missing_patient_id']==1
    assert report['checks']['invalid_date']==1
    pd.testing.assert_frame_equal(df,original)
def test_identical_distributions_zero():
    assert psi(range(100),range(100))==pytest.approx(0)
def test_shift_and_constant_reference_detected():
    assert psi(range(100),range(1000,1100))>0
    assert psi([5]*20,[50]*20)>0
def test_missing_values_drift():
    assert psi([None,np.inf], [1,2]) is None
def test_schema_rejected():
    with pytest.raises(ValueError): assess(pd.DataFrame({'amount':[1]}))
