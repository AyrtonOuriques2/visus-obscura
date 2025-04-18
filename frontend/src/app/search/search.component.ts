import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {
  urlToSearch: string = '';

  constructor(private apiService: ApiService){}

  analyseUrl() {
    this.apiService.analyseUrl(this.urlToSearch).subscribe((response) => {
      console.log(response);
    })
  }

}
