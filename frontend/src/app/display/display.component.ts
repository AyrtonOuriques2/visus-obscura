import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatOption, MatSelect, MatSelectTrigger } from '@angular/material/select';
import { MatTooltip } from '@angular/material/tooltip';

@Component({
  selector: 'app-display',
  imports: [
    MatCardModule,
    CommonModule,
    MatTooltip,
    MatFormField,
    MatSelect,
    MatOption,
    MatSelectTrigger
  ],
  standalone: true,
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.css'] 
})
export class DisplayComponent {

  @Input() data: any;
  selectedReportType = "protocols"

  constructor() {}

  
  ngOnInit() {
    console.log(this.data); 
  }
}
