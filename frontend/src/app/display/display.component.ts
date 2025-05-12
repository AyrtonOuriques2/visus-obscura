import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatTooltip } from '@angular/material/tooltip';

@Component({
  selector: 'app-display',
  imports: [
    MatCardModule,
    CommonModule,
    MatTooltip
  ],
  standalone: true,
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.css'] 
})
export class DisplayComponent {

  @Input() data: any;

  constructor() {}

  
  ngOnInit() {
    console.log(this.data); 
  }
}
