import psycopg2 

class Database():

    """
    To handle connections to Database.
    """

    def __init__(self, 
                 dbname: str,
                 user: str, 
                 password: str, 
                 host: str = 'localhost', 
                 port: int = 5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port


    def get_db_url(self):
        """
        Get string connection with the defined class arguments.
        """
        
        db_url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

        return db_url


    def get_connection(self):
        """
        Connects to Database using the string connection
        """

        db_url = self.get_db_url()
        self.db_url = db_url

        self.conn = psycopg2.connect(self.db_url)
        return self.conn
