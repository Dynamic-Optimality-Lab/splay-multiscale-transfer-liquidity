"""Support-uniform comparison features, all identically zero when A=B."""
def transform(f,n):
    import numpy as np
    v=f.astype(np.int32);return np.stack((v[:,0]-v[:,1],v[:,2]-v[:,3],v[:,4]-v[:,5],v[:,6]-v[:,7],n-v[:,8],n-v[:,9],v[:,0]+v[:,1]+2*n-2*v[:,10],v[:,11],v[:,2]+v[:,3]-2*v[:,12],v[:,4]+v[:,5]-2*v[:,13],v[:,0]+v[:,1]+2*n-2*v[:,14],v[:,16],n-v[:,17],v[:,18],n-v[:,19]),axis=1)
def quadratic(v):
    import numpy as np
    return np.stack([v[:,i] for i in range(15)]+[v[:,i]*v[:,j] for i in range(15) for j in range(i,15)],axis=1)
