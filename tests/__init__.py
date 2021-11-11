from vektonn.dtos import VectorDto

vektonn_local_base_url = 'http://localhost:8081'

data_source_name = 'Samples.DenseVectors'
data_source_version = '0.1'

index_name = 'Samples.DenseVectors'
index_version = '0.1'

zero_vector = VectorDto(is_sparse=False, coordinates=[0.0, 0.0])
