from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Model1, Model2, Contact
from .serializers import Model1Serializer, Model2Serializer, ContactSerializer
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime


class Model1ViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Model1 - requires authentication
    """
    def get_queryset(self):
        return Model1.objects.all()
    
    serializer_class = Model1Serializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the model first
        model1_instance = serializer.save(created_by=self.request.user)
        
        # Send email notification after creation
        try:
            self.send_creation_email(model1_instance)
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
    
    def send_creation_email(self, model1_instance):
        """
        Send email notification when Model1 is created
        """
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = f"New Model1 Created: {model1_instance.name}"
        message = f"""
        A new Model1 item has been created:
        
        Name: {model1_instance.name}
        Description: {model1_instance.description[:100]}...
        Created by: {model1_instance.created_by.username if model1_instance.created_by else 'Unknown'}
        Created at: {model1_instance.created_at}
        ID: {model1_instance.id}
        
        This is an automated notification.
        """
        
        # You can configure these in your .env file
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
        recipient_list = getattr(settings, 'ADMIN_EMAILS', ['admin@example.com'])
        
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=True  # Don't fail if email sending fails
        )

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)


class Model2ViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Model2 - requires authentication
    """
    def get_queryset(self):
        return Model2.objects.all()
    
    serializer_class = Model2Serializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the model first
        model2_instance = serializer.save(created_by=self.request.user)
        
        # Run the script after creation
        try:
            from .research.run_model2 import process_model2_input
            
            # Prepare input data for the script
            script_input = {
                'title': model2_instance.title,
                'content': model2_instance.content,
                'model_id': model2_instance.id,
                'created_at': model2_instance.created_at.isoformat() if model2_instance.created_at else None,
                'is_active': model2_instance.is_active,
                'action': 'created'
            }
            
            # Run the script
            results = process_model2_input(script_input)
            
            # Log the results (you could also store them in the model)
            print(f"Script executed after Model2 creation: {results}")
            
        except Exception as e:
            # Log error but don't fail the creation
            print(f"Script execution failed after creation: {str(e)}")
        
        # Send email notification
        try:
            self.send_creation_email(model2_instance)
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
    
    def send_creation_email(self, model2_instance):
        """
        Send email notification when Model2 is created
        """
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = f"New Model2 Created: {model2_instance.title}"
        message = f"""
        A new Model2 item has been created:
        
        Title: {model2_instance.title}
        Content: {model2_instance.content[:100]}...
        Created by: {model2_instance.created_by.username if model2_instance.created_by else 'Unknown'}
        Created at: {model2_instance.created_at}
        ID: {model2_instance.id}
        
        This is an automated notification.
        """
        
        # You can configure these in your .env file
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
        recipient_list = getattr(settings, 'ADMIN_EMAILS', ['admin@example.com'])
        
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=True  # Don't fail if email sending fails
        )

    def perform_update(self, serializer):
        # Save the model first
        model2_instance = serializer.save(created_by=self.request.user)
        
        # Run the script after update
        try:
            from .research.run_model2 import process_model2_input
            
            # Prepare input data for the script
            script_input = {
                'title': model2_instance.title,
                'content': model2_instance.content,
                'model_id': model2_instance.id,
                'created_at': model2_instance.created_at.isoformat() if model2_instance.created_at else None,
                'is_active': model2_instance.is_active,
                'action': 'updated'
            }
            
            # Run the script
            results = process_model2_input(script_input)
            
            # Log the results
            print(f"Script executed after Model2 update: {results}")
            
        except Exception as e:
            print(f"Script execution failed after update: {str(e)}")
        
        # Send update notification email
        try:
            self.send_update_email(model2_instance)
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
    
    def send_update_email(self, model2_instance):
        """
        Send email notification when Model2 is updated
        """
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = f"Model2 Updated: {model2_instance.title}"
        message = f"""
        A Model2 item has been updated:
        
        Title: {model2_instance.title}
        Content: {model2_instance.content[:100]}...
        Updated by: {model2_instance.created_by.username if model2_instance.created_by else 'Unknown'}
        Updated at: {model2_instance.updated_at}
        ID: {model2_instance.id}
        
        This is an automated notification.
        """
        
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
        recipient_list = getattr(settings, 'ADMIN_EMAILS', ['admin@example.com'])
        
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=True
        )

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        model2 = self.get_object()
        model2.is_active = not model2.is_active
        model2.save()
        return Response({'is_active': model2.is_active})

    @action(detail=True, methods=['post'])
    def run_script(self, request, pk=None):
        """
        Run the run_model2.py script with the current Model2 data
        """
        try:
            model2 = self.get_object()
            
            # Prepare input data for the script
            script_input = {
                'title': model2.title,
                'content': model2.content,
                'model_id': model2.id,
                'created_at': model2.created_at.isoformat() if model2.created_at else None,
                'is_active': model2.is_active
            }
            
            # Import the script function
            from .research.run_model2 import process_model2_input
            
            # Run the script
            results = process_model2_input(script_input)
            
            # Add model information to results
            results['model_info'] = {
                'id': model2.id,
                'title': model2.title,
                'created_at': model2.created_at.isoformat() if model2.created_at else None,
                'is_active': model2.is_active
            }
            
            return Response({
                'message': 'Script executed successfully',
                'results': results,
                'model_id': model2.id
            })
            
        except ImportError as e:
            return Response({
                'error': f'Failed to import script: {str(e)}',
                'message': 'Script execution failed'
            }, status=500)
        except Exception as e:
            return Response({
                'error': f'Script execution failed: {str(e)}',
                'message': 'Script execution failed'
            }, status=500)

    @action(detail=False, methods=['post'])
    def run_script_with_input(self, request):
        """
        Run the run_model2.py script with custom input data
        """
        try:
            # Get input data from request
            title = request.data.get('title', '')
            content = request.data.get('content', '')
            
            if not title or not content:
                return Response({
                    'error': 'Both title and content are required',
                    'message': 'Invalid input data'
                }, status=400)
            
            # Prepare input data for the script
            script_input = {
                'title': title,
                'content': content,
                'input_type': 'custom',
                'timestamp': datetime.now().isoformat()
            }
            
            # Import the script function
            from .research.run_model2 import process_model2_input
            
            # Run the script
            results = process_model2_input(script_input)
            
            return Response({
                'message': 'Script executed successfully with custom input',
                'results': results,
                'input_data': script_input
            })
            
        except ImportError as e:
            return Response({
                'error': f'Failed to import script: {str(e)}',
                'message': 'Script execution failed'
            }, status=500)
        except Exception as e:
            return Response({
                'error': f'Script execution failed: {str(e)}',
                'message': 'Script execution failed'
            }, status=500)


class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Contact - no authentication required for creation
    """
    def get_queryset(self):
        return Contact.objects.all()
    
    serializer_class = ContactSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        contact = self.get_object()
        contact.is_read = True
        contact.save()
        return Response({'is_read': True})


class PublicAPIViewSet(viewsets.ViewSet):
    """
    Public API endpoints - no authentication required
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def health_check(self, request):
        return Response({
            'status': 'healthy',
            'message': 'Backend API is running'
        })

    @action(detail=False, methods=['get'])
    def public_info(self, request):
        from django.conf import settings
        return Response({
            'app_name': 'Full Stack App',
            'version': '1.0.0',
            'description': 'Django + Vue.js application with OIDC authentication',
            'mode': getattr(settings, 'MODE', 'LOCAL')
        })


@method_decorator(csrf_exempt, name='dispatch')
class AuthViewSet(viewsets.ViewSet):
    """
    Authentication endpoints
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def user(self, request):
        if request.user.is_authenticated:
            # Get additional U-M specific attributes if available
            user_data = {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_authenticated': True
            }
            
            # Add U-M specific attributes if they exist
            if hasattr(request.user, 'oidc_profile'):
                oidc_profile = request.user.oidc_profile
                if hasattr(oidc_profile, 'eduperson_principal_name'):
                    user_data['umich_id'] = oidc_profile.eduperson_principal_name
                if hasattr(oidc_profile, 'eduperson_affiliation'):
                    user_data['affiliation'] = oidc_profile.eduperson_affiliation
                if hasattr(oidc_profile, 'edumember_is_member_of'):
                    user_data['member_of'] = oidc_profile.edumember_is_member_of
            
            return Response(user_data)
        else:
            return Response({
                'is_authenticated': False
            }, status=401)



    @action(detail=False, methods=['post'])
    def mock_login(self, request):
        """
        Mock login for local development - reads user from file when MODE=LOCAL
        """
        from django.conf import settings
        
        if getattr(settings, 'MODE', 'LOCAL') != 'LOCAL':
            return Response({'error': 'Mock login only available in LOCAL mode'}, status=400)
        
        try:
            # Read mock user data from a simple JSON file
            import json
            import os
            
            mock_user_file = os.path.join(settings.BASE_DIR, 'mock_user.json')
            
            if os.path.exists(mock_user_file):
                with open(mock_user_file, 'r') as f:
                    mock_data = json.load(f)
            else:
                # Default mock user if file doesn't exist
                mock_data = {
                    'username': 'mockuser',
                    'email': 'mock@umich.edu',
                    'first_name': 'Mock',
                    'last_name': 'User',
                    'umich_id': 'mockuser@umich.edu',
                    'affiliation': 'student',
                    'member_of': ['umich:student']
                }
            
            # Create or get the mock user
            user, created = User.objects.get_or_create(
                username=mock_data['username'],
                defaults={
                    'email': mock_data['email'],
                    'first_name': mock_data['first_name'],
                    'last_name': mock_data['last_name'],
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            
            # Log the user in
            login(request, user)
            
            return Response({
                'message': 'Mock login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'umich_id': mock_data.get('umich_id'),
                    'affiliation': mock_data.get('affiliation'),
                    'member_of': mock_data.get('member_of')
                }
            })
        except Exception as e:
            return Response({'error': f'Mock login failed: {str(e)}'}, status=500)

    @action(detail=False, methods=['post'])
    def mock_logout(self, request):
        """
        Mock logout for local development - only available when MODE=LOCAL
        """
        from django.conf import settings
        
        if getattr(settings, 'MODE', 'LOCAL') != 'LOCAL':
            return Response({'error': 'Mock logout only available in LOCAL mode'}, status=400)
        
        from django.contrib.auth import logout
        
        logout(request)
        return Response({'message': 'Mock logout successful'})
