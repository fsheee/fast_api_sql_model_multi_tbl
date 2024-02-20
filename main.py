from fastapi import FastAPI,HTTPException,Depends,Query
from sqlmodel import SQLModel, create_engine, Session,select
from models import Team,Hero,HeroCreate,HeroResponse,HeroUpdate,TeamCreate,TeamResponse,TeamUpdate,HeroResponsewithTeam
from typing import List,Annotated

# DB_URL="postgresql://fsheekhi:p2SAyY4ftHFv@ep-still-lake-a1tsjpws.ap-southeast-1.aws.neon.tech/apidb?sslmode=require"
DB_URL="postgresql://fsheekhi:p2SAyY4ftHFv@ep-still-lake-a1tsjpws.ap-southeast-1.aws.neon.tech/api_db?sslmode=require"
engine=create_engine(DB_URL)

def create_db_and_tables():
 SQLModel.metadata.create_all(engine)

app = FastAPI()
# DB Dependency Injection
def get_deb():
  with Session(engine) as session:
    yield session

@app.on_event("startup")
def on_startup():
  create_db_and_tables()

@app.get("/")
async def root():
  return{"message":"FAST API WITH PYDNATIC"}

#get all heroes
@app.get("/heros",response_model=List[Hero])
def get_heroes(session:Annotated[Session,Depends(get_deb)],offset:int=Query(default=0,le=4),limit:int=Query(default=0,le=4)):
  
    # heroes=session.exec(select(Hero)).all()
  heroes=session.exec(select(Hero).offset(offset).limit(limit)).all()
  return heroes

# create hero
@app.post("/heroes")  
def create_hero(hero:HeroCreate,db:Annotated[Session,Depends(get_deb)]):
    print ("data from client",hero)
    hero_to_insert=Hero.model_validate(hero)
    print("data after validation",hero_to_insert)
    db.add(hero_to_insert)
    db.commit()
    db.refresh(hero_to_insert)
    # return hero_to_insert
    return {"hero":hero_to_insert,"message" :"Hero has be created "}

#get single hero
# @app.get("/heros/{hero_id}",response_model=HeroResponse)
@app.get("/heros/{hero_id}",response_model=HeroResponsewithTeam)
def get_hero_by_id(hero_id:int,session:Annotated[Session,Depends(get_deb)]):
  hero=session.get(Hero,hero_id)
  if not hero:
    raise HTTPException(status_code=404,detail="Hero ID not found")
  print(hero.team)
  return hero   
                 
  
  # hero update
@app.patch("/heroes/{hero_id}")  
def update_hero(hero_id:int,hero_data:HeroUpdate,session:Annotated[Session,Depends(get_deb)]):
 #get hero
  hero=session.get(Hero,hero_id)
  if not hero:
    raise HTTPException(status_code=404,detail="Hero not found")
  print("Hero in DB",hero)
  print("data from client",hero_data)

  hero_dict_data=hero_data.model_dump(exclude_unset=True)
  print("hero_dict_data",hero_dict_data)

  for key,value in hero_dict_data.items():
    setattr(hero,key,value)

  print("After",hero)  

  session.add(hero)
  session.commit()
  session.refresh(hero)

  return {"message":"Hero updated Successfully"}

                      
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id:int,session:Annotated[Session,Depends(get_deb)]):
  hero=session.get(Hero,hero_id)
  if not hero:
    raise HTTPException(status_code=404,detail="Hero not found")
  session.delete(hero)
  session.commit()
  return {"message":"Hero Delete successfully"}
                        
#get all team
@app.get("/teams",response_model=List[Team])
def get_teams(session:Annotated[Session,Depends(get_deb)],offset:int=Query(default=0,le=4),limit:int=Query(default=0,le=4)):
  teams=session.exec(select(Team).offset(offset).limit(limit)).all()
  return teams                       
                        
# create Team
@app.post("/teams",response_model=TeamResponse)  
def create_team(team:TeamCreate,db:Annotated[Session,Depends(get_deb)]):
    print ("data from client",team)
    team_to_insert=Team.model_validate(team)
    print("data after validation",team_to_insert)
    db.add(team_to_insert)
    db.commit()
    db.refresh(team_to_insert)
    return {"team":team_to_insert,"message" :"Team has be created"}
          
#get single Team
@app.get("/teams/{team_id}",response_model=TeamResponse)
def get_team_by_id(team_id:int,session:Annotated[Session,Depends(get_deb)]):
  team=session.get(Team,team_id)
  if not Team:
    raise HTTPException(status_code=404,detail="Team ID not found")
  return team                   
  
  # team update
@app.patch("/teams/{team_id}")  
def update_team(team_id:int,team_data:TeamUpdate,session:Annotated[Session,Depends(get_deb)]):
 #get team
  team=session.get(Team,team_id)
  if not team:
    raise HTTPException(status_code=404,detail="Hero not found")
  print("Team in DB",team)
  print("data from client",team_data)

  team_dict_data=team_data.model_dump(exclude_unset=True)
  print("team_dict_data",team_dict_data)

  for key,value in team_dict_data.items():
    setattr(team,key,value)

  print("After",team)  

  session.add(team)
  session.commit()
  session.refresh(team)

  return {"message":"Team updated Successfully"}

                      
@app.delete("/teams/{team_id}")
def delete_team(team_id:int,session:Annotated[Session,Depends(get_deb)]):
  team=session.get(Hero,team_id)
  if not team:
    raise HTTPException(status_code=404,detail="Team not found")
  session.delete(team)
  session.commit()
  return {"message":"Team Delete successfully"}
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        

