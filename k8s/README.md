# Kubernetes Scripts
These scripts are for producing Digital Earth Africa products.

# COG script
 The process of converting USGS Collection 2 data to COGs and indexing into ODC is described in [Indexing USGS Collection 2 Data](https://docs.dev.dea.ga.gov.au/procedures/indexing_collection2.html?highlight=sqs%20consume%20py).
 The yaml `eo-datasets-job.yaml`  spins up a Kubernetes job to covert the collection 2 data to COGs.
 The job is started with;
```
kubectl apply -f eo-datasets-job.yaml
```
and can be monitored with;
```
kubectl get jobs
```

