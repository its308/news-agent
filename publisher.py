# from wordpress_xmlrpc import Client,WordPressPost
# from wordpress_xmlrpc.methods.posts import NewPost
# import logging # production level error handling
#
# # WordPress is a tool for building websites!
#
# class WordPressPublisher:
#     def __init__(self,wp_url,username,password):
#         try:
#             self.client=Client(wp_url,username, password)
#             logging.info("Connected to wordPress SuccessFully!")
#         except Exception as e:
#             logging.error(f"Failed to connect to WordPress: {str(e)}")
#             raise  #it stops the further execution of programme
#
#     def publish(self,title,content,seo_data=None,image=None):
#         try:
#             post=WordPressPost
#             post.title=title
#             post.content=content
#
#             if seo_data:
#                 post.excerpt=seo_data.get("meta_description","")
#                 post.terms_names={
#                     'post_tag':seo_data.get('keywords',[])
#                 }
#
#             post.post_status='publish'
#
#             post_id=self.client.call(NewPost(post))
#             logging.info(f"Published article {title} with ID {post_id}")
#
#             if image:
#                 self._upload_image(image)
#
#             return post_id
#
#         except Exception as e:
#             logging.error(f"Failed to publish article {title}: {str(e)}")
#
#     def _upload_image(self,image_path):
#         try:
#             from wordpress_xmlrpc.methods.media import UploadFile
#
#             with open(image_path,'rb') as img_file:
#                 data={
#                     'name':image_path.split('/')[-1],
#                     'type':'image.jpeg',
#                     'bits':img_file.read()
#                 }
#                 response=self.client.call(UploadFile(data))
#                 logging.info(f"Uploaded image file:{response['url']}")
#
#                 return response['id']
#
#         except Exception as e:
#             logging.error(f"Failed to upload image '{image_path}': {str(e)}")
# publisher.py
import json
import logging

class WordPressPublisher:
    def __init__(self):
        self.output_file = "output.json"

    def publish(self, title, content, seo_data=None):
        """Save articles as drafts in a local file"""
        try:
            article = {
                "title": title,
                "content": content,
                "seo_data": seo_data
            }

            # Append the article to the output file
            with open(self.output_file, "a") as f:
                json.dump(article, f)
                f.write("\n")

            logging.info(f"Draft saved locally: {title}")
            return True

        except Exception as e:
            logging.error(f"Failed to save draft: {str(e)}")
            return False


