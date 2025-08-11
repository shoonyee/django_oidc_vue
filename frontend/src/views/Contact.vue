<template>
  <div>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-6">
          <v-card-title class="text-h4 text-center mb-6">
            <v-icon left>mdi-email</v-icon>
            Contact Us
          </v-card-title>
          
          <v-card-text class="text-body-1">
            <p class="mb-6 text-center">
              Have a question or need assistance? Fill out the form below and we'll get back to you as soon as possible.
            </p>
            
            <v-form @submit.prevent="submitContact" ref="contactFormRef">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="contactForm.name"
                    label="Full Name"
                    required
                    variant="outlined"
                    :rules="[rules.required]"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="contactForm.email"
                    label="Email Address"
                    type="email"
                    required
                    variant="outlined"
                    :rules="[rules.required, rules.email]"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-text-field
                    v-model="contactForm.subject"
                    label="Subject"
                    required
                    variant="outlined"
                    :rules="[rules.required]"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-textarea
                    v-model="contactForm.message"
                    label="Message"
                    required
                    variant="outlined"
                    rows="6"
                    :rules="[rules.required, rules.minLength]"
                    placeholder="Please describe your inquiry or question in detail..."
                  ></v-textarea>
                </v-col>
              </v-row>
              
              <v-card-actions class="justify-center pt-6">
                <v-btn
                  type="submit"
                  color="primary"
                  size="large"
                  :loading="loading"
                  :disabled="loading"
                >
                  <v-icon left>mdi-send</v-icon>
                  Send Message
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
        </v-card>
        
        <!-- Contact Information -->
        <v-card class="mt-6" variant="outlined">
          <v-card-title class="text-h6">
            <v-icon left>mdi-information</v-icon>
            Additional Information
          </v-card-title>
          
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <div class="text-center">
                  <v-icon size="48" color="primary" class="mb-2">mdi-map-marker</v-icon>
                  <h4 class="text-h6 mb-2">Address</h4>
                  <p class="text-body-2">
                    University of Michigan<br>
                    Ann Arbor, MI 48109
                  </p>
                </div>
              </v-col>
              
              <v-col cols="12" md="4">
                <div class="text-center">
                  <v-icon size="48" color="primary" class="mb-2">mdi-email</v-icon>
                  <h4 class="text-h6 mb-2">Email</h4>
                  <p class="text-body-2">
                    support@example.com<br>
                    info@example.com
                  </p>
                </div>
              </v-col>
              
              <v-col cols="12" md="4">
                <div class="text-center">
                  <v-icon size="48" color="primary" class="mb-2">mdi-phone</v-icon>
                  <h4 class="text-h6 mb-2">Phone</h4>
                  <p class="text-body-2">
                    +1 (734) 555-0123<br>
                    Mon-Fri 9AM-5PM EST
                  </p>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Success Dialog -->
    <v-dialog v-model="successDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h6 text-center">
          <v-icon color="success" class="mr-2">mdi-check-circle</v-icon>
          Message Sent!
        </v-card-title>
        
        <v-card-text class="text-center">
          Thank you for your message. We'll get back to you as soon as possible.
        </v-card-text>
        
        <v-card-actions class="justify-center">
          <v-btn
            color="primary"
            @click="successDialog = false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'Contact',
  setup() {
    const contactForm = ref({
      name: '',
      email: '',
      subject: '',
      message: ''
    })
    
    const loading = ref(false)
    const successDialog = ref(false)
    const contactFormRef = ref(null)
    
    const rules = {
      required: v => !!v || 'This field is required',
      email: v => /.+@.+\..+/.test(v) || 'Please enter a valid email address',
      minLength: v => v.length >= 10 || 'Message must be at least 10 characters long'
    }
    
    const submitContact = async () => {
      if (!contactFormRef.value.validate()) return
      
      loading.value = true
      try {
        await axios.post('/api/contact/', contactForm.value)
        
        // Reset form
        contactForm.value = {
          name: '',
          email: '',
          subject: '',
          message: ''
        }
        
        // Show success dialog
        successDialog.value = true
        
        // Reset form validation
        contactFormRef.value.resetValidation()
      } catch (error) {
        console.error('Error submitting contact form:', error)
        // You could show an error message here
      } finally {
        loading.value = false
      }
    }
    
    return {
      contactForm,
      loading,
      successDialog,
      contactFormRef,
      rules,
      submitContact
    }
  }
}
</script>
