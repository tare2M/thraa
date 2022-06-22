import matplotlib.pyplot as plt 
import base64
from io import BytesIO 

def get_graph():
  buffer=BytesIO()
  plt.savefig(buffer,format='png')
  buffer.seek(0)
  image_png=buffer.getvalue()
  graph=base64.b64encode(image_png)
  graph=graph.decode('utf-8')
  buffer.close()
  return graph

def get_plot(x,y,z,u,v,b):
 plt.switch_backend('AGG')

	
 plt.xlabel('Generation')
 plt.ylabel('Fitness')
 plt.figure(figsize=(15,8))
 plt.plot(x,y,'o-')
 plt.plot(x,z,c='red')
 plt.plot(x,u,c='black')
 plt.plot(x,v,c='Green')
 plt.plot(x,b,c='Yellow')
 plt.xticks(rotation=45)
 plt.tight_layout()
 plt.grid(True)	
 plt.legend(["Gens","Max Value","Min Value","Average Value","Best Value"])
 graph=get_graph()
 return graph 
