import tweepy
import networkx as nx
import config
from collections import defaultdict
import csv
from time import sleep

# OAuth認証部分
CK	  = config.CONSUMER_KEY
CS	  = config.CONSUMER_SECRET
AT	  = config.ACCESS_TOKEN
ATS	 = config.ACCESS_TOKEN_SECRET

id_list=[]

with open('user_id.csv', 'r', newline='') as f:
	reader = csv.reader(f,lineterminator='\n')
	for r in reader:
		id_list.append(int(r[0]))


# フォロワー取得
def getFollowers_ids(api, id):
	# Get Id list of followers
	followers_ids = tweepy.Cursor(api.followers_ids, id=id, cursor=-1).items()
	followers_ids_list = []
	try:
		followers_ids_list = [followers_id for followers_id in followers_ids]
	except tweepy.error.TweepError as e:
		print(e.reason)
	return followers_ids_list
 

def main():
	#API認証
	auth = tweepy.OAuthHandler(CK, CS)
	auth.set_access_token(AT, ATS)
	api = tweepy.API(auth, wait_on_rate_limit=True)
	
	center_to_followers = {}
	node_attrs = defaultdict(dict)
	
	G = nx.DiGraph()
	
	
	'''
	# フォロワーを取得したいアカウント複数
	CENTER_ACCOUNTS = ['lensenizm','2PxQYq85y0bjOxJ','EEjyanaiaka']
	for center_screen_name in CENTER_ACCOUNTS:
		# get center account information (node attributes)
		center_info = api.get_user(screen_name=center_screen_name)
		# get id of center account

		center_id = center_info.id
	'''
	print("start")

	'''
	この方法の問題点：id_listのユーザが凍結・削除されていたら
	center_info = api.get_user(center_id)
	でエラーが起こりプログラムが止まってしまう
	（あまりないとは思うが）
	→tryで解決済み（外側いらないかも）

	たぶん有向グラフになっていない
	→Gのほうはなってる
	'''

	follower_id_list={}

	try:
		for center_id in id_list:
			try:
				center_info = api.get_user(center_id)	#cender_idの情報
			except Exception as e:
				print(e)
			else:
				print("center_id:")
				print(center_id)
				G.add_node(center_id)

				node_attrs[center_id]['screenName'] = center_info.screen_name
				node_attrs[center_id]['followersNum'] = center_info.followers_count
				node_attrs[center_id]['followNum'] = center_info.friends_count
			
				# フォロワー一覧取得，リツイートしてるユーザも欲しいならidを追加
				#たぶん15回/15分　→1回/1分なので1分sleepすればいい？
				center_to_followers[center_id] = getFollowers_ids(api=api, id=center_id)

				tmp=[]
				print("target")
			
				# set empty value to account attribute that is not center
				for follower_id in center_to_followers[center_id]:
					if (follower_id in id_list) == True:
						print(follower_id)
						G.add_node(follower_id)
						G.add_edge(center_id,follower_id)
						node_attrs.setdefault(follower_id, {'screenName': '', 'followersNum': '', 'followNum': ''})
						tmp.append(follower_id)

				print("target list")

				follower_id_list[center_id]=tmp
				print(follower_id_list[center_id])
		
			sleep(1 * 60)
			print("end sleep")

	except Exception as e:
		print(e)

	finally:
		graph = nx.from_dict_of_lists(follower_id_list)
		nx.set_node_attributes(graph, node_attrs)
		nx.write_gml(G,'Graph.gml')
		nx.write_gml(graph, 'twitter.gml')# ソーシャルグラフの作成 
		# nx.readwrite.gml.read_gml("twitter.gml") とすれば，グラフを読み込むことが可能
		print("all finish")
		
 
if __name__ == "__main__":
	main()

