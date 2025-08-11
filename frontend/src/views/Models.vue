<template>
  <div>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6">
          <v-card-title class="text-h4 text-center mb-6">
            Models Overview
          </v-card-title>
          
          <v-card-text class="text-body-1">
            <p class="mb-6 text-center">
              Explore the different models in our application. Each model provides different functionality and data management capabilities.
            </p>
            
            <v-row>
              <v-col cols="12" md="6">
                <v-card
                  to="/models/model1"
                  hover
                  class="h-100"
                  color="primary"
                  dark
                >
                  <v-card-title class="text-h5">
                    <v-icon left>mdi-database</v-icon>
                    Model 1
                  </v-card-title>
                  
                  <v-card-text>
                    <p>Manage basic data entries with names and descriptions.</p>
                    <v-chip
                      v-if="model1Count !== null"
                      color="white"
                      text-color="primary"
                      class="mt-2"
                    >
                      {{ model1Count }} entries
                    </v-chip>
                  </v-card-text>
                  
                  <v-card-actions>
                    <v-btn
                      text
                      color="white"
                      to="/models/model1"
                    >
                      View Details
                      <v-icon right>mdi-arrow-right</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-card
                  to="/models/model2"
                  hover
                  class="h-100"
                  color="secondary"
                  dark
                >
                  <v-card-title class="text-h5">
                    <v-icon left>mdi-file-document</v-icon>
                    Model 2
                  </v-card-title>
                  
                  <v-card-text>
                    <p>Manage content with titles, text, and active status.</p>
                    <v-chip
                      v-if="model2Count !== null"
                      color="white"
                      text-color="secondary"
                      class="mt-2"
                    >
                      {{ model2Count }} entries
                    </v-chip>
                  </v-card-text>
                  
                  <v-card-actions>
                    <v-btn
                      text
                      color="white"
                      to="/models/model2"
                    >
                      View Details
                      <v-icon right>mdi-arrow-right</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
            
            <v-divider class="my-6"></v-divider>
            
            <v-alert
              type="info"
              variant="tonal"
              class="mb-4"
            >
              <strong>Note:</strong> model2 requires authentication to access. Please log in with your U-M credentials to view and manage the data.
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Models',
  setup() {
    const model1Count = ref(null)
    const model2Count = ref(null)
    
    const fetchCounts = async () => {
      try {
        // These endpoints require authentication, so we'll handle errors gracefully
        const [model1Response, model2Response] = await Promise.allSettled([
          axios.get('/api/model1/'),
          axios.get('/api/model2/')
        ])
        
        if (model1Response.status === 'fulfilled') {
          model1Count.value = model1Response.value.data.length
        }
        
        if (model2Response.status === 'fulfilled') {
          model2Count.value = model2Response.value.data.length
        }
      } catch (error) {
        console.log('Counts not available without authentication')
      }
    }
    
    onMounted(() => {
      fetchCounts()
    })
    
    return {
      model1Count,
      model2Count
    }
  }
}
</script>
