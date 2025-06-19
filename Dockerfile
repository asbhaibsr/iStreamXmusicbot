# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# System dependencies
RUN apt update && apt install -y ffmpeg git && apt clean

# Copy all files to container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Ye WALI LINE use karni hai sirf
RUN pip install git+https://github.com/pytgcalls/pytgcalls

# Expose port for uptime ping
EXPOSE 8080

# Run bot
CMD ["python3", "bot.py"]
