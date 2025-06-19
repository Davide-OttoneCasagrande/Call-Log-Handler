# Use the official Elasticsearch image as a base
FROM docker.elastic.co/elasticsearch/elasticsearch:8.17.1

# Set environment variables
ENV discovery.type=single-node \
    xpack.security.enabled=false \
    bootstrap.memory_lock=true \
    ES_JAVA_OPTS="-Xms1g -Xmx1g"

# Create and set permissions for the Elasticsearch data directory
#RUN mkdir -p /usr/share/elasticsearch/data \
#    && chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/data

# Expose necessary ports
EXPOSE 9200 9300

# Define the command to run Elasticsearch
CMD ["/usr/share/elasticsearch/bin/elasticsearch"]
