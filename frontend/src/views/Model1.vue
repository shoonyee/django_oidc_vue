<template>
  <div>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6">
          <v-card-title class="text-h4 mb-6">
            <v-icon left>mdi-database</v-icon>
            Model 1 Management
          </v-card-title>
          
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
                      v-model="newEntry.name"
                      label="Name"
                      required
                      variant="outlined"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="6">
                    <v-textarea
                      v-model="newEntry.description"
                      label="Description"
                      required
                      variant="outlined"
                      rows="3"
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
              >
                <template v-slot:item.actions="{ item }">
                  <v-btn
                    icon
                    small
                    color="primary"
                    @click="editEntry(item.raw)"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  
                  <v-btn
                    icon
                    small
                    color="error"
                    @click="deleteEntry(item.raw.id)"
                    class="ml-2"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Edit Dialog -->
    <v-dialog v-model="editDialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h6">
          Edit Entry
        </v-card-title>
        
        <v-card-text>
          <v-form @submit.prevent="updateEntry">
            <v-text-field
              v-model="editingEntry.name"
              label="Name"
              required
              variant="outlined"
              class="mb-4"
            ></v-text-field>
            
            <v-textarea
              v-model="editingEntry.description"
              label="Description"
              required
              variant="outlined"
              rows="3"
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
  name: 'Model1',
  setup() {
    const entries = ref([])
    const loading = ref(false)
    const search = ref('')
    const editDialog = ref(false)
    const editingEntry = ref({})
    
    const newEntry = ref({
      name: '',
      description: ''
    })
    
    const headers = [
      { title: 'Name', key: 'name' },
      { title: 'Description', key: 'description' },
      { title: 'Created', key: 'created_at' },
      { title: 'Updated', key: 'updated_at' },
      { title: 'Actions', key: 'actions', sortable: false }
    ]
    
    const filteredEntries = computed(() => {
      if (!search.value) return entries.value
      return entries.value.filter(entry => 
        entry.name.toLowerCase().includes(search.value.toLowerCase()) ||
        entry.description.toLowerCase().includes(search.value.toLowerCase())
      )
    })
    
    const fetchEntries = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/model1/')
        entries.value = response.data
      } catch (error) {
        console.error('Error fetching entries:', error)
      } finally {
        loading.value = false
      }
    }
    
    const createEntry = async () => {
      if (!newEntry.value.name || !newEntry.value.description) return
      
      loading.value = true
      try {
        await axios.post('/api/model1/', newEntry.value)
        await fetchEntries()
        newEntry.value = { name: '', description: '' }
      } catch (error) {
        console.error('Error creating entry:', error)
      } finally {
        loading.value = false
      }
    }
    
    const editEntry = (entry) => {
      editingEntry.value = { ...entry }
      editDialog.value = true
    }
    
    const updateEntry = async () => {
      loading.value = true
      try {
        await axios.put(`/api/model1/${editingEntry.value.id}/`, editingEntry.value)
        await fetchEntries()
        editDialog.value = false
        editingEntry.value = {}
      } catch (error) {
        console.error('Error updating entry:', error)
      } finally {
        loading.value = false
      }
    }
    
    const deleteEntry = async (id) => {
      if (!confirm('Are you sure you want to delete this entry?')) return
      
      loading.value = true
      try {
        await axios.delete(`/api/model1/${id}/`)
        await fetchEntries()
      } catch (error) {
        console.error('Error deleting entry:', error)
      } finally {
        loading.value = false
      }
    }
    
    // Fetch entries on component mount
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
      fetchEntries,
      createEntry,
      editEntry,
      updateEntry,
      deleteEntry
    }
  }
}
</script>
