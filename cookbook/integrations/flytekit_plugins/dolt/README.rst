Dolt: Data versioning
===============================================


Installation
------------

.. code:: bash

   pip install flytekitplugins.dolt

Quick Start
-----------

.. testcode:: dolt-quickstart

   doltdb_path = os.path.join(os.path.dirname(__file__), "foo")

   user_conf = DoltConfig(
       db_path=doltdb_path,
       tablename="users",
   )

   @task
   def populate_users(a: int) -> DoltTable:
       users = [("George", a), ("Alice", a*2), ("Stephanie", a*3)]
       df = pd.DataFrame(users, columns=["name", "count"])
       return DoltTable(data=df, config=user_conf)

   @task
   def count_users(table: DoltTable) -> pandas.DataFrame:
       return table.data

   @workflow
   def wf(a: int) -> pandas.DataFrame:
       users = populate_users(a=a)
       return users

   print(wf(a=2))

.. testoutput:: pandera-quickstart
   :options: +NORMALIZE_WHITESPACE

              name  count
   0  Stephanie     21
   1     George      7
   2      Alice     14
