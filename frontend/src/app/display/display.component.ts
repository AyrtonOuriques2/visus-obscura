import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-display',
  imports: [
    MatCardModule,
    CommonModule
  ],
  standalone: true,
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.css'] 
})
export class DisplayComponent {

  @Input() data: any;

  constructor() {}

  objectKeys = Object.keys;
  
  ngOnInit() {
    console.log(this.data); 
  }
}
