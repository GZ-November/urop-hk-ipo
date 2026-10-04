"""Validate jackknife inference against independent statistical invariants."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pricing_topic1_completion_2026 import cv3


def test_intercept_cluster_mean_variance():
    # Equal-sized clusters: variance of the grand mean is s^2(cluster means)/G.
    means=np.array([1.,4.,-2.,8.,3.,6.]);y=np.repeat(means,3)
    x=np.ones((len(y),1));g=np.repeat(np.arange(len(means)),3)
    b,v,_,gap=cv3(y,x,g)
    assert b[0]==pytest.approx(means.mean())
    assert v[0,0]==pytest.approx(means.var(ddof=1)/len(means))
    assert gap<1e-12


def test_duplicate_rows_in_each_cluster_preserves_cv3():
    y=np.array([2.,5.,1.,8.,3.,7.,4.,-1.]);x=np.c_[np.ones(8),np.arange(8)]
    g=np.repeat(np.arange(4),2)
    b,v,_,_=cv3(y,x,g)
    bd,vd,_,_=cv3(np.repeat(y,2),np.repeat(x,2,axis=0),np.repeat(g,2))
    np.testing.assert_allclose(b,bd,atol=1e-12)
    np.testing.assert_allclose(v,vd,atol=1e-12)


def test_delete_cluster_rank_loss_is_rejected():
    x=np.array([[1.,0.],[1.,0.],[1.,1.],[1.,1.]])
    with pytest.raises(ValueError,match='Singular deleted cluster'):
        cv3(np.array([1.,2.,4.,6.]),x,np.array([0,0,1,1]))
