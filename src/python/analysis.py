from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from signal_processing.features import windowed_mfccs
import definitions

def kmeans_quantize_distances(df, cluster_by, cluster_ratio=0.3):
    new_df = df.copy()
    X = np.array([np.asarray(x) for x in df[cluster_by]])
    K = int(len(X) * cluster_ratio)
    kmeans = KMeans(n_clusters=K, random_state=0).fit(X)
    transformed = kmeans.transform(X)
    labels = np.argmin(transformed, axis=1)
    for idx, label in enumerate(labels):
        new_df.loc[idx, 'label'] = label
        new_df.loc[idx, 'distance'] = transformed[idx, label]
    return new_df

def sparsify_df(df, n_clusters, column_names):
    # Standardize the specified columns
    scaler = StandardScaler()
    scaled_columns = scaler.fit_transform(df[column_names])
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(scaled_columns)
    cluster_assignments = kmeans.labels_
    representative_samples = []
    for i in range(n_clusters):
        # Get the indices of data points belonging to the current cluster
        cluster_indices = np.where(cluster_assignments == i)[0]
        # Find the index of the data point closest to the cluster center
        center = kmeans.cluster_centers_[i]
        closest_index = cluster_indices[np.argmin(np.linalg.norm(scaled_columns[cluster_indices] - center, axis=1))]
        representative_samples.append(df.iloc[closest_index])
    sparser_df = pd.DataFrame(representative_samples)
    sparser_df.reset_index(drop=True, inplace=True)
    return sparser_df

