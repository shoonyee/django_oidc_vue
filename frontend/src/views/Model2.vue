<template>
  <div>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6">
          <v-card-title class="text-h4 mb-6">
            <v-icon left>mdi-file-document</v-icon>
            Model 2 Management
          </v-card-title>
          
          <!-- Success Notification -->
          <v-alert
            v-if="notification.show"
            :type="notification.type"
            :text="notification.message"
            closable
            @click:close="notification.show = false"
            class="mb-4"
          ></v-alert>
          
          <!-- Script Execution Results -->
          <v-card v-if="lastScriptResults" class="mb-4" variant="outlined">
            <v-card-title class="text-h6">
              <v-icon left>mdi-code-braces</v-icon>
              Last Script Execution Results
            </v-card-title>
            <v-card-text>
              <pre class="bg-grey-lighten-4 pa-3 rounded">{{ JSON.stringify(lastScriptResults, null, 2) }}</pre>
            </v-card-text>
          </v-card>
          

          
          <!-- Create New Entry -->
          <v-card class="mb-6" variant="outlined">
            <v-card-title class="text-h6">
              Create New Entry
            </v-card-title>
            
            <v-card-text>
              <v-form @submit.prevent="createEntry">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="newEntry.title"
                      label="Title"
                      required
                      variant="outlined"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-switch
                      v-model="newEntry.is_active"
                      label="Active"
                      color="success"
                    ></v-switch>
                  </v-col>
                  
                  <v-col cols="12">
                    <v-textarea
                      v-model="newEntry.content"
                      label="Content"
                      required
                      variant="outlined"
                      rows="4"
                    ></v-textarea>
                  </v-col>
                </v-row>
                
                <v-card-actions>
                  <v-btn
                    type="submit"
                    color="primary"
                    :loading="loading"
                  >
                    Create Entry
                  </v-btn>
                </v-card-actions>
              </v-form>
            </v-card-text>
          </v-card>
          
          <!-- Entries List -->
          <v-card>
            <v-card-title class="text-h6">
              Existing Entries
              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
                variant="outlined"
                density="compact"
                style="max-width: 300px"
              ></v-text-field>
            </v-card-title>
            
            <v-card-text>
              <v-data-table
                :headers="headers"
                :items="filteredEntries"
                :loading="loading"
                :search="search"
                class="elevation-1"
                :items-per-page="10"
                :items-per-page-options="[5, 10, 25, 50]"
                show-current-page
                show-items-per-page
              >
                <!-- Loading state -->
                <template v-slot:loading>
                  <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
                </template>
                
                <!-- Empty state -->
                <template v-slot:no-data>
                  <div class="text-center pa-4">
                    <v-icon size="64" color="grey">mdi-database-off</v-icon>
                    <div class="text-h6 mt-2">No entries found</div>
                    <div class="text-body-2 text-grey">Create your first entry above</div>
                  </div>
                </template>
                <template v-slot:item.is_active="{ item }">
                  <v-chip
                    v-if="item && item.is_active !== undefined"
                    :color="item.is_active ? 'success' : 'error'"
                    :text="item.is_active ? 'Active' : 'Inactive'"
                    size="small"
                  ></v-chip>
                  <span v-else class="text-grey">N/A</span>
                </template>
                
                <template v-slot:item.actions="{ item }">
                  <div v-if="item" class="d-flex align-center">
                    <v-btn
                      icon
                      small
                      :color="item.is_active ? 'warning' : 'success'"
                      @click="toggleActive(item)"
                      :loading="item.toggling"
                      :disabled="!item.id"
                    >
                      <v-icon>
                        {{ item.is_active ? 'mdi-pause' : 'mdi-play' }}
                      </v-icon>
                    </v-btn>
                    
                    <v-btn
                      icon
                      small
                      color="primary"
                      @click="editEntry(item)"
                      class="ml-2"
                      :disabled="!item.id"
                    >
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    
                    <v-btn
                      icon
                      small
                      color="error"
                      @click="deleteEntry(item.id)"
                      class="ml-2"
                      :disabled="!item.id"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </div>
                  <span v-else class="text-grey">N/A</span>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Edit Dialog -->
    <v-dialog v-model="editDialog" max-width="700px">
      <v-card>
        <v-card-title class="text-h6">
          Edit Entry
        </v-card-title>
        
        <v-card-text>
          <v-form @submit.prevent="updateEntry">
            <v-text-field
              v-model="editingEntry.title"
              label="Title"
              required
              variant="outlined"
              class="mb-4"
            ></v-text-field>
            
            <v-switch
              v-model="editingEntry.is_active"
              label="Active"
              color="success"
              class="mb-4"
            ></v-switch>
            
            <v-textarea
              v-model="editingEntry.content"
              label="Content"
              required
              variant="outlined"
              rows="6"
            ></v-textarea>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            text
            @click="editDialog = false"
          >
            Cancel
          </v-btn>
          
          <v-btn
            color="primary"
            @click="updateEntry"
            :loading="loading"
          >
            Update
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Model2',
  setup() {
    const entries = ref([])
    const loading = ref(false)
    const search = ref('')
    const editDialog = ref(false)
    const editingEntry = ref({})
    
    const newEntry = ref({
      title: '',
      content: '',
      is_active: true
    })
    
    const notification = ref({
      show: false,
      type: 'success',
      message: ''
    })
    
    const lastScriptResults = ref(null)
    
    const showNotification = (type, message) => {
      notification.value = {
        show: true,
        type,
        message
      }
      // Auto-hide after 5 seconds
      setTimeout(() => {
        notification.value.show = false
      }, 5000)
    }
    
    const headers = [
      { title: 'Title', key: 'title', sortable: true },
      { title: 'Content', key: 'content', sortable: true },
      { title: 'Status', key: 'is_active', sortable: true },
      { title: 'Created', key: 'created_at', sortable: true },
      { title: 'Updated', key: 'updated_at', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, width: '200px' }
    ]
    
    const filteredEntries = computed(() => {
      if (!search.value) return entries.value
      return entries.value.filter(entry => 
        entry.title.toLowerCase().includes(search.value.toLowerCase()) ||
        entry.content.toLowerCase().includes(search.value.toLowerCase())
      )
    })
    
    const fetchEntries = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/model2/')
        entries.value = response.data.map(entry => ({
          ...entry,
          toggling: false,
          // Ensure all required fields are present
          id: entry.id,
          title: entry.title || '',
          content: entry.content || '',
          is_active: entry.is_active !== undefined ? entry.is_active : true,
          created_at: entry.created_at || '',
          updated_at: entry.updated_at || '',
          created_by: entry.created_by || null
        }))
        console.log('Fetched entries:', entries.value)
      } catch (error) {
        console.error('Error fetching entries:', error)
        showNotification('error', 'Failed to fetch entries')
      } finally {
        loading.value = false
      }
    }
    
    const createEntry = async () => {
      if (!newEntry.value.title || !newEntry.value.content) return
      
      loading.value = true
      try {
        // Use perform_create action to trigger post-creation actions
        const response = await axios.post('/api/model2/', newEntry.value)
        
        // Show success message with details about what happened
        console.log('✅ Entry created successfully!')
        console.log('📧 Email notification sent to admins')
        console.log('🔧 Script executed with new data')
        console.log('📊 Script results:', response.data)
        
        // Store script results for display
        if (response.data && response.data.results) {
          lastScriptResults.value = {
            action: 'Created',
            timestamp: new Date().toLocaleString(),
            results: response.data.results
          }
        }
        
        // Show success notification to user
        showNotification('success', `Entry created successfully! Script executed and email notification sent.`)
        
        // Refresh the entries list
        await fetchEntries()
        
        // Reset the form
        newEntry.value = { title: '', content: '', is_active: true }
        
      } catch (error) {
        console.error('❌ Error creating entry:', error)
        // Show error notification to user
        let errorMessage = 'Failed to create entry'
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        }
        showNotification('error', errorMessage)
        
        if (error.response) {
          console.error('Server response:', error.response.data)
        }
      } finally {
        loading.value = false
      }
    }
    
    const toggleActive = async (entry) => {
      if (!entry || !entry.id) {
        console.error('Invalid entry for toggle:', entry)
        showNotification('error', 'Invalid entry data')
        return
      }
      
      entry.toggling = true
      try {
        await axios.post(`/api/model2/${entry.id}/toggle_active/`)
        entry.is_active = !entry.is_active
        showNotification('success', `Entry ${entry.is_active ? 'activated' : 'deactivated'} successfully`)
      } catch (error) {
        console.error('Error toggling status:', error)
        showNotification('error', 'Failed to toggle entry status')
      } finally {
        entry.toggling = false
      }
    }
    
    const editEntry = (entry) => {
      if (!entry || !entry.id) {
        console.error('Invalid entry for edit:', entry)
        showNotification('error', 'Invalid entry data')
        return
      }
      
      editingEntry.value = { ...entry }
      editDialog.value = true
    }
    
    const updateEntry = async () => {
      loading.value = true
      try {
        // Use perform_update action to trigger post-update actions
        const response = await axios.put(`/api/model2/${editingEntry.value.id}/`, editingEntry.value)
        
        // Show success message with details about what happened
        console.log('✅ Entry updated successfully!')
        console.log('📧 Update email notification sent to admins')
        console.log('🔧 Script executed with updated data')
        console.log('📊 Script results:', response.data)
        
        // Store script results for display
        if (response.data && response.data.results) {
          lastScriptResults.value = {
            action: 'Updated',
            timestamp: new Date().toLocaleString(),
            results: response.data.results
          }
        }
        
        // Show success notification to user
        showNotification('success', `Entry updated successfully! Script executed and update email notification sent.`)
        
        // Refresh the entries list
        await fetchEntries()
        
        // Close the edit dialog
        editDialog.value = false
        
      } catch (error) {
        console.error('❌ Error updating entry:', error)
        // Show error notification to user
        let errorMessage = 'Failed to update entry'
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        }
        showNotification('error', errorMessage)
        
        if (error.response) {
          console.error('Server response:', error.response.data)
        }
      } finally {
        loading.value = false
      }
    }
    
    const deleteEntry = async (id) => {
      if (!id) {
        console.error('Invalid ID for delete:', id)
        showNotification('error', 'Invalid entry ID')
        return
      }
      
      if (!confirm('Are you sure you want to delete this entry?')) return
      
      loading.value = true
      try {
        await axios.delete(`/api/model2/${id}/`)
        showNotification('success', 'Entry deleted successfully')
        await fetchEntries()
      } catch (error) {
        console.error('Error deleting entry:', error)
        showNotification('error', 'Failed to delete entry')
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      fetchEntries()
    })
    
    return {
      entries,
      loading,
      search,
      editDialog,
      editingEntry,
      newEntry,
      headers,
      filteredEntries,
      notification,
      lastScriptResults,
      createEntry,
      toggleActive,
      editEntry,
      updateEntry,
      deleteEntry
    }
  }
}
</script>
