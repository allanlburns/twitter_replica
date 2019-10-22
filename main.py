from app import app

# The way to run Flask on a separate port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)
