# Use the official Kibana base image
FROM docker.elastic.co/kibana/kibana:8.17.1

# Set environment variables for Kibana
ENV ELASTICSEARCH_HOSTS=http://elasticsearch:9200

# Expose Kibana's default port
EXPOSE 5601

# Define the command to start Kibana
CMD ["/usr/share/kibana/bin/kibana"]
