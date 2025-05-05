from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.core.mail import send_mail
from django.conf import settings
from person.models import User

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = []  # No permission restrictions

    def get_queryset(self):
        queryset = Post.objects.all()
        
        # Get filters from query parameters
        user_id = self.request.query_params.get('user_id')
        post_type = self.request.query_params.get('type')
        
        # Apply filters if they exist
        if user_id:
            queryset = queryset.filter(author_id=user_id)
        if post_type:
            queryset = queryset.filter(type=post_type)
            
        return queryset

    def post(self, request, *args, **kwargs):
        # Get filters from request body
        author_id = request.data.get('author', None)
        post_type = request.data.get('type', None)
        
        queryset = self.filter_queryset(self.get_queryset())
        
        # Apply filters if they exist
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if post_type:
            queryset = queryset.filter(type=post_type)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = self.perform_create(serializer)
        
        # Send email notifications to tagged users
        tags = request.data.get('tags', [])
        if tags:
            self.send_tag_notifications(post, tags)
            
        return Response({
            'message': 'Post created successfully',
            'post': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def send_tag_notifications(self, post, tags):
        print("\n=== Email Settings Debug ===")
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        print("=== End Email Settings Debug ===\n")

        print("\n=== Email Notification Debug ===")
        for username in tags:
            try:
                user = User.objects.get(username=username)
                if user.email:  # Only send if user has an email
                    subject = f'You were mentioned in a post'
                    message = f'''
                    Hi {user.username},

                    You were mentioned in a post by {post.author.username}.

                    Post Title: {post.title}
                    Content: {post.content}


                    Best regards,
                    Connect Alumni Team
                    '''
                    print(f"\nAttempting to send email to {user.email} for post mention")
                    print(f"Using FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
                    
                    try:
                        # Try sending with explicit from_email
                        send_mail(
                            subject,
                            message,
                            from_email=settings.DEFAULT_FROM_EMAIL,  # Use settings from django.conf
                            recipient_list=[user.email],
                            fail_silently=False,
                        )
                        print(f" Successfully sent email to {user.email}")
                    except Exception as e:
                        print(f" Failed to send email to {user.email}")
                        print(f"Error details: {str(e)}")
                        print(f"Email settings: FROM_EMAIL={settings.DEFAULT_FROM_EMAIL}")
                else:
                    print(f" User {username} has no email address configured")
            except User.DoesNotExist:
                print(f" User {username} not found in database")
                continue  # Skip if user doesn't exist
        print("=== End Email Notification Debug ===\n")

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

class PostLikeView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, pk):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            message = 'Post unliked successfully'
        else:
            post.likes.add(request.user)
            message = 'Post liked successfully'
        return Response({
            'message': message,
            'post': self.get_serializer(post).data
        }, status=status.HTTP_200_OK)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer)
        return Response({
            'message': 'Comment created successfully',
            'comment': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            post_id=self.kwargs['post_pk']
        ) 